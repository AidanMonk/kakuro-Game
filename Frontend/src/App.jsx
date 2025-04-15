import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import Main from './components/mainComponent/main';
import SignUp from './components/mainComponent/SignUp';
import './App.css';

// Component to handle scrolling
function ScrollToTop() {
  const { pathname } = useLocation();

  useEffect(() => {
    // Enable scrolling on body when component mounts or route changes
    document.body.style.overflow = 'auto';
    document.body.style.height = 'auto';
    document.documentElement.style.overflow = 'auto';
    document.documentElement.style.height = 'auto';

    // Scroll to top on route change
    window.scrollTo(0, 0);

    return () => {
      // Ensure scrolling is enabled when component unmounts
      document.body.style.overflow = 'auto';
      document.documentElement.style.overflow = 'auto';
    };
  }, [pathname]);

  return null;
}

function App() {
  // Force enable scrolling on initial load
  useEffect(() => {
    document.body.style.overflow = 'auto';
    document.body.style.height = 'auto';
    document.documentElement.style.overflow = 'auto';
    document.documentElement.style.height = 'auto';

    // Add event listener to constantly check and re-enable scrolling if needed
    const checkScrolling = () => {
      if (document.body.style.overflow === 'hidden') {
        document.body.style.overflow = 'auto';
      }
      if (document.documentElement.style.overflow === 'hidden') {
        document.documentElement.style.overflow = 'auto';
      }
    };

    const interval = setInterval(checkScrolling, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <Router>
      <div className="App">
        <ScrollToTop />
        <Routes>
          <Route path='/' element={<SignUp />} />
          <Route path='/game' element={<Main />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;