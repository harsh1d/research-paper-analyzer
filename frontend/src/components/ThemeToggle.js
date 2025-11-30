/**
 * Theme Toggle Component with Animation
 */

import React from 'react';
import { useTheme } from '../context/ThemeContext';
import './ThemeToggle.css';

function ThemeToggle() {
  const { isDarkMode, toggleTheme } = useTheme();

  return (
    <button 
      className="theme-toggle" 
      onClick={toggleTheme}
      aria-label="Toggle theme"
    >
      <div className={`toggle-track ${isDarkMode ? 'dark' : 'light'}`}>
        <div className="toggle-thumb">
          {isDarkMode ? (
            <span className="icon moon">🌙</span>
          ) : (
            <span className="icon sun">☀️</span>
          )}
        </div>
      </div>
      <span className="toggle-label">
        {isDarkMode ? 'Dark' : 'Light'}
      </span>
    </button>
  );
}

export default ThemeToggle;
