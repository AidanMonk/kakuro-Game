import React, { useState, useEffect } from 'react';
import { useSoundManager } from './SoundManager';
import './Settings.css'; // Import the CSS file we created

const Settings = ({ onApplySettings }) => {
  const [showPanel, setShowPanel] = useState(false);
  const [settings, setSettings] = useState({
    theme: 'default',
    soundEffects: true,
    musicVolume: 50,
    difficulty: 'medium',
    animations: true,
  });

  // Get sound manager from context
  const soundManager = useSoundManager();

  // Initialize settings from sound manager
  useEffect(() => {
    if (soundManager) {
      setSettings(prev => ({
        ...prev,
        soundEffects: soundManager.soundEnabled,
        musicVolume: soundManager.musicVolume
      }));
    }
  }, [soundManager]);

  // When settings change, notify parent component
  useEffect(() => {
    if (onApplySettings) {
      onApplySettings(settings);
    }
  }, [settings, onApplySettings]);

  const togglePanel = () => {
    setShowPanel(!showPanel);
    if (soundManager) {
      soundManager.play('click');
    }
  };

  const handleSettingChange = (setting, value) => {
    setSettings({
      ...settings,
      [setting]: value,
    });

    // Apply changes immediately
    if (soundManager) {
      switch(setting) {
        case 'theme':
          applyTheme(value);
          soundManager.play('click');
          break;
        case 'soundEffects':
          soundManager.toggleSoundEffects(value);
          // Play a test sound if enabling sound
          if (value) soundManager.play('click');
          break;
        case 'musicVolume':
          soundManager.setVolume(value);
          break;
        default:
          soundManager.play('click');
          break;
      }
    } else {
      if (setting === 'theme') {
        applyTheme(value);
      }
    }
  };

  const applyTheme = (theme) => {
    const body = document.querySelector('body');

    // Remove existing theme classes
    body.classList.remove('theme-default', 'theme-blue', 'theme-green', 'theme-purple');

    // Apply selected theme
    switch (theme) {
      case 'blue':
        body.style.backgroundColor = '#2c5784';
        break;
      case 'green':
        body.style.backgroundColor = '#3a6a47';
        break;
      case 'purple':
        body.style.backgroundColor = '#593a6a';
        break;
      default: // Default/brown theme
        body.style.backgroundColor = 'rgb(127, 78, 47)';
        break;
    }
  };

  return (
    <>
      {/* Settings Icon */}
      <div className="settings-icon" onClick={togglePanel}>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z"/>
        </svg>
      </div>

      {/* Settings Panel */}
      {showPanel && (
        <div className="settings-panel">
          <h3>Settings</h3>
          <button className="close-settings" onClick={togglePanel}>×</button>

          {/* Theme Setting */}
          <div className="settings-option">
            <label>Theme</label>
            <div className="theme-option">
              <div
                className={`theme-preview theme-default ${settings.theme === 'default' ? 'selected' : ''}`}
                onClick={() => handleSettingChange('theme', 'default')}
                title="Default"
              ></div>
              <div
                className={`theme-preview theme-blue ${settings.theme === 'blue' ? 'selected' : ''}`}
                onClick={() => handleSettingChange('theme', 'blue')}
                title="Blue"
              ></div>
              <div
                className={`theme-preview theme-green ${settings.theme === 'green' ? 'selected' : ''}`}
                onClick={() => handleSettingChange('theme', 'green')}
                title="Green"
              ></div>
              <div
                className={`theme-preview theme-purple ${settings.theme === 'purple' ? 'selected' : ''}`}
                onClick={() => handleSettingChange('theme', 'purple')}
                title="Purple"
              ></div>
            </div>
          </div>

          {/* Sound Effects Toggle */}
          <div className="settings-option">
            <div className="toggle-container">
              <label>Sound Effects</label>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.soundEffects}
                  onChange={(e) => handleSettingChange('soundEffects', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>
          </div>

          {/* Music Volume */}
          <div className="settings-option">
            <label>Music Volume: {settings.musicVolume}%</label>
            <input
              type="range"
              min="0"
              max="100"
              value={settings.musicVolume}
              onChange={(e) => handleSettingChange('musicVolume', parseInt(e.target.value))}
            />
          </div>

          {/* Default Difficulty */}
          <div className="settings-option">
            <label>Default Difficulty</label>
            <select
              value={settings.difficulty}
              onChange={(e) => handleSettingChange('difficulty', e.target.value)}
            >
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          {/* Animations Toggle */}
          <div className="settings-option">
            <div className="toggle-container">
              <label>Animations</label>
              <label className="toggle-switch">
                <input
                  type="checkbox"
                  checked={settings.animations}
                  onChange={(e) => handleSettingChange('animations', e.target.checked)}
                />
                <span className="slider"></span>
              </label>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default Settings;