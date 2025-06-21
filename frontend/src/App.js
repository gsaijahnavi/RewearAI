import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Mycloset  from './Pages/Mycloset.js';
import OOTD from './Pages/OOTD.js';
import Secondhand from './Pages/Secondhand.js';
import BottomNav from './Components/BottomNav';

function App() {
  return (
    <Router>
    <div>
      <div style={{ paddingBottom: '60px' }}>
         <Routes>
          <Route path="/Mycloset" element={<Mycloset />} />
          <Route path="/OOTD" element={<OOTD />} />
          <Route path="/Secondhand" element={<Secondhand />} />
        </Routes>
      </div>

      <BottomNav />
    </div>
    </Router>
  );
}
export default App;
