import { useState, useEffect } from "react";
import "./Board.css";
import GamePopup from "./GamePopup";
import { useSoundManager } from './SoundManager';

const Board = ({ difficulty, onNewGame }) => {
  // state variables
  const [board, setBoard] = useState(null);
  const [boardId, setBoardId] = useState(null);
  const [editingCell, setEditingCell] = useState(null);
  const [currentDifficulty, setCurrentDifficulty] = useState(difficulty || "medium");
  const [hintsUsed, setHintsUsed] = useState(0);
  const [popup, setPopup] = useState(null);
  const [showInstructions, setShowInstructions] = useState(false);
  const [loading, setLoading] = useState(false);
  const [isInitialLoad, setIsInitialLoad] = useState(true);

  // Get sound manager
  const soundManager = useSoundManager();

  const updateCellValue = (row, col, value) => {
    // Validate input: must be a number between 1 and 9
    if (!value || isNaN(value) || value < 1 || value > 9) return;

    // Play sound
    if (soundManager) {
      soundManager.play('click');
    }

    // Create a new updated board by mapping over rows and columns
    const updatedBoard = board.map((r, rIdx) => {
      return r.map((cell, cIdx) => {
        // Update only the selected cell if it's a number
        if (rIdx === row && cIdx === col && cell.type === "number") {
          return { ...cell, value: parseInt(value, 10) };
        }
        return cell;
      });
    });

    setBoard(updatedBoard);
    setEditingCell(null);
  };

  // Effect to load the board when component mounts or difficulty changes
  useEffect(() => {
    // Only change difficulty when the prop changes
    if (difficulty !== currentDifficulty) {
      setCurrentDifficulty(difficulty);
    }

    // Only initialize the board on first load or when difficulty changes
    if (isInitialLoad || difficulty !== currentDifficulty) {
      const initializeBoard = async () => {
        setLoading(true);
        try {
          console.log("Initializing board with difficulty:", currentDifficulty);

          const response = await fetch("http://127.0.0.1:8000/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ difficulty: currentDifficulty }),
          });

          if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
          }

          const data = await response.json();
          console.log("Received board data:", data);
          setBoard(data.board);
          setBoardId(data.board_id);  // Save the board ID
          console.log("Board loaded with difficulty:", data.difficulty, "Board ID:", data.board_id);

          // Reset hints used for new board
          setHintsUsed(0);

          // Mark that initial load is complete
          setIsInitialLoad(false);

          // Play sound when board is loaded
          if (soundManager) {
            soundManager.play('click');
          }
        } catch (error) {
          console.error("Error initializing board:", error);
        } finally {
          setLoading(false);
        }
      };

      initializeBoard();
    }
  }, [currentDifficulty, difficulty, isInitialLoad, soundManager]);

  const validateBoard = async () => {
    // Play click sound
    if (soundManager) {
      soundManager.play('click');
    }

    // Check for empty cells first
    let hasEmptyCells = false;

    board.forEach(row => {
      row.forEach(cell => {
        if (cell.type === "number" && cell.value === 0) {
          hasEmptyCells = true;
        }
      });
    });

    if (hasEmptyCells) {
      if (soundManager) {
        soundManager.play('wrong');
      }

      setPopup({
        type: 'error',
        message: 'You have empty cells. Please fill in all cells before checking your answer.',
        onClose: () => setPopup(null)
      });
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/validate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ board }), // Send the current board state
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();

      if (data.is_valid) {
        // Play victory sound for correct answer
        if (soundManager) {
          soundManager.play('victory');
        }

        setPopup({
          type: 'success',
          message: 'Congratulations! You solved the puzzle correctly!',
          onAction: onNewGame
        });
      } else {
        // Play wrong sound for incorrect answer
        if (soundManager) {
          soundManager.play('wrong');
        }

        setPopup({
          type: 'error',
          message: 'Sorry, your solution is incorrect. Some of the numbers don\'t match the required sums.',
          onClose: () => setPopup(null)
        });
      }
    } catch (error) {
      console.error("Error validating board:", error);
      setPopup({
        type: 'error',
        message: 'Error validating the board. Please try again.',
        onClose: () => setPopup(null)
      });
    }
  };

  const getHint = async () => {
    // Play hint sound
    if (soundManager) {
      soundManager.play('hint');
    }

    // Prevent getting hints if the limit is reached
    if (hintsUsed >= 3) {
      setPopup({
        type: 'error',
        message: "You've used all available hints!",
        onClose: () => setPopup(null)
      });
      return;
    }

    // Find all empty number cells (value = 0)
    const emptyCells = [];

    board.forEach((row, rowIndex) => {
      row.forEach((cell, colIndex) => {
        if (cell.type === "number" && cell.value === 0) {
          emptyCells.push({ row: rowIndex, col: colIndex });
        }
      });
    });

    // If no empty cells, show message
    if (emptyCells.length === 0) {
      setPopup({
        type: 'info',
        message: "No empty cells left to give hints for!",
        onClose: () => setPopup(null)
      });
      return;
    }

    // Get a random empty cell
    const randomIndex = Math.floor(Math.random() * emptyCells.length);
    const randomCell = emptyCells[randomIndex];

    try {
      console.log("Requesting hint for board:", boardId, "cell:", randomCell);

      // Request a hint from the server
      const response = await fetch("http://127.0.0.1:8000/hint/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          board_id: boardId,
          row: randomCell.row,
          col: randomCell.col
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Received hint data:", data);

      // Create a new board with the hint
      const updatedBoard = board.map((r, rIdx) => {
        return r.map((cell, cIdx) => {
          if (rIdx === data.row && cIdx === data.col) {
            return { ...cell, value: data.hint_value };
          }
          return cell;
        });
      });

      setBoard(updatedBoard);
      setHintsUsed(hintsUsed + 1);

      // Show hint popup
      setPopup({
        type: 'hint',
        message: `Hint: Value ${data.hint_value} added to row ${data.row + 1}, column ${data.col + 1}`,
        onClose: () => setPopup(null)
      });
    } catch (error) {
      console.error("Error getting hint:", error);
      setPopup({
        type: 'error',
        message: "Error getting hint. Please try again.",
        onClose: () => setPopup(null)
      });
    }
  };

  // Toggle instructions popup
  const toggleInstructions = () => {
    if (soundManager) {
      soundManager.play('click');
    }
    setShowInstructions(!showInstructions);
  };

  // Handle cell click with sound
  const handleCellClick = (cell, rowIndex, colIndex) => {
    if (cell.type === "number") {
      if (soundManager) {
        soundManager.play('click');
      }
      setEditingCell({ row: rowIndex, col: colIndex });
    }
  };

  // Force a new board (for the "New Game" button)
  const handleNewGame = () => {
    // Set isInitialLoad to true to force a board reload
    setIsInitialLoad(true);
    // Then call the parent's onNewGame function
    if (onNewGame) {
      onNewGame();
    }
  };

  // Show loading message until board data is available
  if (loading || !board) return <p className="loading-text">Loading {currentDifficulty} board...</p>;

  return (
    <div className="board">
      <div className="difficulty-badge">
        Level: {currentDifficulty}
      </div>
      <div className="table-container">
        <table>
          <tbody>
            {board.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((cell, colIndex) => {
                  const isEditing = editingCell?.row === rowIndex && editingCell?.col === colIndex;

                  return (
                    <td
                      key={colIndex}
                      className={`cell ${cell.type}`}
                      onClick={() => handleCellClick(cell, rowIndex, colIndex)}
                    >
                      {cell.type === "sum" && (
                        <div className="sum-cell">
                          {cell.right_sum !== null && `→${cell.right_sum}`}
                          <br />
                          {cell.down_sum !== null && `↓${cell.down_sum}`}
                        </div>
                      )}

                      {cell.type === "number" && (
                        <div className="number-cell">
                          {isEditing ? (
                            <input
                              type="number"
                              min="1"
                              max="9"
                              autoFocus
                              style={{ appearance: "textfield" }}
                              className="input-number-box"
                              onBlur={(e) => updateCellValue(rowIndex, colIndex, e.target.value)}
                              onKeyDown={(e) => {
                                if (e.key === "Enter") {
                                  updateCellValue(rowIndex, colIndex, e.target.value);
                                }
                              }}
                            />
                          ) : (
                            cell.value !== 0 && <span>{cell.value}</span>
                          )}
                        </div>
                      )}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="board-buttons">
        <button onClick={validateBoard} className="btn check-btn">Check Answer</button>
        {hintsUsed < 3 ? (
          <button onClick={getHint} className="btn hint-btn">Get Hint ({3 - hintsUsed} left)</button>
        ) : (
          <button disabled className="btn hint-btn disabled">No Hints Left</button>
        )}
        <button onClick={handleNewGame} className="new-game-btn">New Game</button>
        <button onClick={toggleInstructions} className="how-to-play-btn">How to Play</button>
      </div>

      {/* Popup component */}
      {popup && (
        <GamePopup
          type={popup.type}
          message={popup.message}
          onClose={popup.onClose}
          onAction={popup.onAction}
        />
      )}

      {/* Instructions popup */}
      {showInstructions && (
        <div className="instructions-popup">
          <div className="instructions-content">
            <h2>HOW TO PLAY?</h2>
            <p>
              Kakuro is a fun and simple number puzzle game! Your goal is to fill the empty boxes in the grid with numbers from 1 to 9 so that the sums match the clues provided. Each clue represents the total you need to achieve in its corresponding row or column. The trick is that numbers in a row or column can't repeat, so you need to think carefully about how to distribute them. Use logic and deduction to figure out the right numbers, and have fun solving the puzzle!
            </p>
            <button className="close-btn" onClick={toggleInstructions}>×</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Board;