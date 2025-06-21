// src/components/BottomNav.js
import { BiCloset } from "react-icons/bi";
import { GiClothes } from "react-icons/gi";
import { PiPackageBold } from "react-icons/pi";
import { Link } from "react-router-dom";
import './BottomNav.css';

function BottomNav() {
  return (
    <div className="bottom-nav">
      <Link to="/mycloset" className="nav-item">
        <BiCloset />
        <span>Mycloset</span>
      </Link>
      <Link to="/ootd" className="nav-item">
        <GiClothes />
        <span>OOTD</span>
      </Link>
      <Link to="/secondhand" className="nav-item">
        <PiPackageBold />
        <span>Secondhand</span>
      </Link>
    </div>
  );
}

export default BottomNav;
