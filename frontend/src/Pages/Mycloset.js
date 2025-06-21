import './Mycloset.css';

const wardrobe = {
  Tops: ["/top1.png", "/top2.png"],
  Bottoms: ["/bottom1.png", "/bottom2.png"],
  Shoes: ["/shoes1.png"],
  Accessories: ["/hat1.png", "/glasses1.png"]
};

function Mycloset() {
  return (
    <div className="mycloset-container">
      <div className="profile-header">
        <img src="/백지헌.png" className="profile-pic" alt="profile" />
        <div className="profile-info">
          <h2 className="username">Seha</h2>
          <div className="follow-stats">
            <span><strong>23</strong> Following</span>
            <span><strong>88</strong> Followers</span>
          </div>
        </div>
      </div>

      <h2 className="title">My Closet</h2>

      {/* 🔽 옷장 */}
      {Object.entries(wardrobe).map(([category, items]) => (
        <div key={category} className={`section-block ${category.toLowerCase()}`}>
          <h3>{category}</h3>
          <div className="item-grid">
            {items.map((src, i) => (
              <img key={i} src={src} className="closet-item" alt={`${category}-${i}`} />
            ))}
            <div className="closet-item add-btn">+</div>
          </div>
        </div>
      ))}
    </div>
  );
}

export default Mycloset;
