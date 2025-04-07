import { useState, useEffect, createContext, useContext } from 'react';

// Import sound assets
import clickSound from '../../assets/click.mp3';
import correctSound from '../../assets/correct.mp3';
import wrongSound from '../../assets/wrong.mp3';
import hintSound from '../../assets/hint.mp3';
import victorySound from '../../assets/victory.mp3';
import backgroundMusic from '../../assets/background-music.mp3';

// Create a context for the sound manager
const SoundContext = createContext();

export const useSoundManager = () => useContext(SoundContext);

export const SoundProvider = ({ children }) => {
  const [sounds, setSounds] = useState({});
  const [music, setMusic] = useState(null);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [musicVolume, setMusicVolume] = useState(0.5);
  const [initialized, setInitialized] = useState(false);

  // Initialize sounds
  useEffect(() => {
    if (!initialized) {
      // Create Audio objects for each sound
      const soundEffects = {
        click: new Audio(clickSound),
        correct: new Audio(correctSound),
        wrong: new Audio(wrongSound),
        hint: new Audio(hintSound),
        victory: new Audio(victorySound)
      };

      // Create background music
      const bgMusic = new Audio(backgroundMusic);
      bgMusic.loop = true;

      // Set initial volume
      Object.values(soundEffects).forEach(sound => {
        sound.volume = musicVolume;
      });
      bgMusic.volume = musicVolume;

      // Save to state
      setSounds(soundEffects);
      setMusic(bgMusic);
      setInitialized(true);
    }
  }, [initialized, musicVolume]);

  // Auto-start music once initialized if sound is enabled
  useEffect(() => {
    if (initialized && soundEnabled && music) {
      // Try to play music automatically
      const playPromise = music.play();

      // Handle autoplay restrictions
      if (playPromise !== undefined) {
        playPromise.catch(error => {
          console.log("Autoplay prevented. User interaction needed to start audio:", error);
          // We'll try again when user interacts with the page
        });
      }
    }
  }, [initialized, soundEnabled, music]);

  // Play a sound effect if enabled
  const play = (soundName) => {
    if (soundEnabled && sounds[soundName]) {
      try {
        sounds[soundName].currentTime = 0; // Restart the sound

        // Try to play the sound
        const playPromise = sounds[soundName].play();

        // Try to start music too if it's not playing
        if (music && music.paused) {
          music.play().catch(e => console.log("Music autoplay still restricted"));
        }

        // Handle errors
        if (playPromise !== undefined) {
          playPromise.catch(e => console.log("Audio play error:", e));
        }
      } catch (error) {
        console.error("Error playing sound:", error);
      }
    }
  };

  // Start background music
  const startMusic = () => {
    if (music && soundEnabled) {
      music.play().catch(e => console.log("Music play error:", e));
    }
  };

  // Pause background music
  const pauseMusic = () => {
    if (music) {
      music.pause();
    }
  };

  // Toggle sound effects on/off
  const toggleSoundEffects = (enabled) => {
    setSoundEnabled(enabled);
    if (!enabled) {
      pauseMusic();
    } else {
      startMusic();
    }
  };

  // Adjust music volume (0-1)
  const setVolume = (volume) => {
    const newVolume = volume / 100; // Convert from percentage
    setMusicVolume(newVolume);

    // Update music volume
    if (music) {
      music.volume = newVolume;

      // Also try to start music if it's not playing yet
      if (soundEnabled && music.paused) {
        music.play().catch(e => console.log("Music play error:", e));
      }
    }

    // Update sound effects volume
    Object.values(sounds).forEach(sound => {
      sound.volume = newVolume;
    });
  };

  // Clean up on unmount
  useEffect(() => {
    return () => {
      if (music) {
        music.pause();
        music.currentTime = 0;
      }
    };
  }, [music]);

  // Value to be provided to consumers
  const value = {
    play,
    startMusic,
    pauseMusic,
    toggleSoundEffects,
    setVolume,
    soundEnabled,
    musicVolume: musicVolume * 100 // Convert to percentage for UI
  };

  return (
    <SoundContext.Provider value={value}>
      {children}
    </SoundContext.Provider>
  );
};

export default SoundContext;