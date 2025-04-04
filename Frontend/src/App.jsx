import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Main from './components/mainComponent/main';
import SignUp from './components/mainComponent/SignUp';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path='/' element={<SignUp />} />
          <Route path='/game' element={<Main />} />
        </Routes>

      </div>
    </Router>

  );
}

export default App;