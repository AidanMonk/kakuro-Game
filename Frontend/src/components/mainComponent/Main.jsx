import React, { useState, useEffect } from 'react'
import { assets } from '../../assets/assets'
import './Main.css'
import Board from './Board'
import DifficultySelection from './DifficultySelection'
import Settings from './Settings'
import { SoundProvider, useSoundManager } from './SoundManager'

const MainContent = () => {
    const [gameStarted, setGameStarted] = useState(false);
    const [difficulty, setDifficulty] = useState(null);
    const [showInstructions, setShowInstructions] = useState(false);
    const [appSettings, setAppSettings] = useState({
        theme: 'default',
        soundEffects: true,
        musicVolume: 50,
    });

    // Get sound manager
    const soundManager = useSoundManager();

    // Set a default difficulty if none is selected
    useEffect(() => {
        if (!difficulty) {
            setDifficulty('medium'); // Default to medium difficulty
        }
    }, [difficulty]);

    // Prevent body scrolling when instructions modal is open
    useEffect(() => {
        if (showInstructions) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = 'auto';
        }

        // Cleanup function to restore scrolling when component unmounts
        return () => {
            document.body.style.overflow = 'auto';
        };
    }, [showInstructions]);

    const handleDifficultySelect = (selectedDifficulty) => {
        if (soundManager) {
            soundManager.play('click');
        }
        setDifficulty(selectedDifficulty);
        setGameStarted(true);

        // Scroll to top when starting a new game
        window.scrollTo(0, 0);
    };

    const handleNewGame = () => {
        if (soundManager) {
            soundManager.play('click');
        }
        setGameStarted(false);
        setDifficulty(null);

        // Scroll to top when starting a new game
        window.scrollTo(0, 0);
    };

    const toggleInstructions = () => {
        if (soundManager) {
            soundManager.play('click');
        }
        setShowInstructions(!showInstructions);
    };

    const handleApplySettings = (newSettings) => {
        setAppSettings(newSettings);
    };

    // Start background music when component mounts
    useEffect(() => {
        if (soundManager && appSettings.soundEffects) {
            soundManager.startMusic();
        }

        return () => {
            if (soundManager) {
                soundManager.pauseMusic();
            }
        };
    }, [soundManager, appSettings.soundEffects]);

    return (
        <>
        <main className={`theme-${appSettings.theme}`}>
            <div className='header'>
                <h1>Welcome to Kakuro Game</h1>
            </div>
            <div className='gameplay'>
                <div className="box">
                    {gameStarted ? (
                        <Board
                            difficulty={difficulty}
                            onNewGame={handleNewGame}
                        />
                    ) : (
                        <>
                            <DifficultySelection
                                onSelectDifficulty={handleDifficultySelect}
                            />
                            <div className="board-buttons difficulty-page-buttons">
                                <button onClick={toggleInstructions} className="how-to-play-btn">How to Play</button>
                            </div>
                        </>
                    )}
                </div>

                <img src={assets.bg1} alt="" />
            </div>

            {/* Settings component */}
            <Settings onApplySettings={handleApplySettings} />

            {/* Instructions popup */}
            {showInstructions && (
                <div className="instructions-popup" onClick={(e) => {
                    // Close popup when clicking outside content
                    if (e.target.className === "instructions-popup") {
                        toggleInstructions();
                    }
                }}>
                    <div className="instructions-content">
                        <h2>HOW TO PLAY?</h2>
                        <p>
                            Kakuro is a fun and simple number puzzle game! Your goal is to fill the empty boxes in the grid with numbers from 1 to 9 so that the sums match the clues provided. Each clue represents the total you need to achieve in its corresponding row or column. The trick is that numbers in a row or column can't repeat, so you need to think carefully about how to distribute them. Use logic and deduction to figure out the right numbers, and have fun solving the puzzle!
                        </p>
                        <button className="close-btn" onClick={toggleInstructions}>×</button>
                    </div>
                </div>
            )}
        </main>
        </>
    );
};

// Wrapper component with SoundProvider
const Main = () => {
    return (
        <SoundProvider>
            <MainContent />
        </SoundProvider>
    );
};

export default Main;