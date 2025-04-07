import React from 'react';
import './GamePopup.css';

const GamePopup = ({ type, message, onClose, onAction }) => {
  // Define different popup types: success, error, hint, info
  const getIcon = () => {
    switch(type) {
      case 'success': return '🎉';
      case 'error': return '❌';
      case 'hint': return '💡';
      case 'info': return 'ℹ️';
      default: return '';
    }
  };

  return (
    <div className="popup-overlay">
      <div className={`popup-container ${type}`}>
        <div className="popup-icon">{getIcon()}</div>
        <div className="popup-message">{message}</div>
        <div className="popup-buttons">
          {onAction && (
            <button className="popup-action-btn" onClick={onAction}>
              {type === 'success' ? 'New Game' : 'OK'}
            </button>
          )}
          {onClose && type !== 'success' && (
            <button className="popup-close-btn" onClick={onClose}>
              Close
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default GamePopup;