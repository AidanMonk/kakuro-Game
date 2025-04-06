import React from 'react';

const DifficultySelection = ({ onSelectDifficulty }) => {
  return (
    <div className="difficulty-container">
      <h2>SELECT DIFFICULTY</h2>
      <div className="difficulty-buttons">
        <button
          className="difficulty-btn easy"
          onClick={() => onSelectDifficulty('easy')}
        >
          EASY
        </button>

        <button
          className="difficulty-btn medium"
          onClick={() => onSelectDifficulty('medium')}
        >
          MEDIUM
        </button>

        <button
          className="difficulty-btn hard"
          onClick={() => onSelectDifficulty('hard')}
        >
          HARD
        </button>
      </div>
    </div>
  );
};

export default DifficultySelection;