import './Secondhand.css';
import { useState } from 'react';

const myClosetItems = [
  { id: 1, name: 'Denim Jacket', image: '/top1.png' },
  { id: 2, name: 'Pleated Skirt', image: '/bottom1.png' },
  { id: 3, name: 'Sneakers', image: '/shoes1.png' },
  { id: 4, name: 'Bucket Hat', image: '/hat1.png' }
];

function Secondhand() {
  const [listedItems, setListedItems] = useState([]);
  const [showCloset, setShowCloset] = useState(false);

  const handleSell = (item) => {
    if (!listedItems.find((i) => i.id === item.id)) {
      setListedItems([...listedItems, { ...item, price: '$25' }]); // 기본 가격 지정
    }
  };

  return (
    <div className="secondhand-container">
      <h2>🛍️ Sell Your Closet</h2>
      <p className="intro">Turn your old favorites into someone else’s new fave ✨</p>

      <div className="listed-section">
        <h3>Your Listed Items</h3>
        {listedItems.length === 0 ? (
          <p className="placeholder">You haven’t listed anything yet!</p>
        ) : (
          <div className="item-grid">
            {listedItems.map((item) => (
              <div key={item.id} className="item-card">
                <img src={item.image} alt={item.name} className="item-image" />
                <h4>{item.name}</h4>
                <p className="price">{item.price}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      <button className="toggle-btn" onClick={() => setShowCloset(!showCloset)}>
        {showCloset ? 'Close Closet' : 'List item from My Closet'}
      </button>

      {showCloset && (
        <div className="closet-section">
          <h3>Select from My Closet</h3>
          <div className="item-grid">
            {myClosetItems.map((item) => (
              <div key={item.id} className="item-card">
                <img src={item.image} alt={item.name} className="item-image" />
                <h4>{item.name}</h4>
                <button className="sell-btn" onClick={() => handleSell(item)}>Sell</button>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Secondhand;
