import { useState, useEffect } from 'react'
import axios from 'axios'

/* ---------------- IMAGE RESOLUTION LOGIC ---------------- */

const normalize = (str = "") =>
  str.toLowerCase().replace(/[^a-z\s]/g, "").trim()

const IMAGE_MAP = [
  {
    keywords: ['cake', 'forest', 'pastry', 'gateau'],
    url: 'https://images.unsplash.com/photo-1578985545062-69928b1d9587'
  },
  {
    keywords: ['chocolate', 'brownie', 'fudge', 'cocoa'],
    url: 'https://images.unsplash.com/photo-1606313564200-e75d5e30476c'
  },
  {
    keywords: ['ice cream', 'icecream', 'kulfi', 'cone', 'shake'],
    url: 'https://images.unsplash.com/photo-1497034825429-c343d7c6a68f'
  },
  {
    keywords: ['ladoo', 'laddu', 'barfi', 'pedha', 'peda', 'jamun', 'mithai', 'indian'],
    url: 'https://images.unsplash.com/photo-1589119908995-c6837fa14848'
  },
  {
    keywords: ['vada', 'vadapav', 'samosa', 'snack', 'namkeen'],
    url: 'https://images.unsplash.com/photo-1601050690597-df0568f70950'
  },
  {
    keywords: ['donut', 'doughnut', 'glazed'],
    url: 'https://images.unsplash.com/photo-1626094309830-26d60ea42f43'
  },
  {
    keywords: ['cookie', 'biscuit'],
    url: 'https://images.unsplash.com/photo-1499636138143-bd649043ea52'
  }
]

const DEFAULT_IMAGE =
  'https://images.unsplash.com/photo-1581798459219-318e76aecc7b'

const getSweetImage = (name = "", category = "") => {
  const text = normalize(`${name} ${category}`)
  const normalizedCategory = normalize(category)

  // 1️⃣ Category-first match (most accurate)
  for (const group of IMAGE_MAP) {
    if (group.keywords.some(k => normalizedCategory.includes(k)))
      return `${group.url}?auto=format&fit=crop&w=500&q=60`
  }

  // 2️⃣ Name-based fallback
  for (const group of IMAGE_MAP) {
    if (group.keywords.some(k => text.includes(k)))
      return `${group.url}?auto=format&fit=crop&w=500&q=60`
  }

  // 3️⃣ Safe default
  return `${DEFAULT_IMAGE}?auto=format&fit=crop&w=500&q=60`
}

/* ---------------- COMPONENT ---------------- */

function SweetsList({ token, searchTerm, role }) {
  const [sweets, setSweets] = useState([])

  const fetchSweets = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/sweets')
      setSweets(res.data)
    } catch (err) {
      console.error("Error fetching sweets:", err)
    }
  }

  useEffect(() => {
    fetchSweets()
  }, [])

  const handleBuy = async (id) => {
    if (!token) {
      alert("Please log in to purchase sweets")
      return
    }

    try {
      await axios.post(
        `http://127.0.0.1:8000/api/sweets/${id}/purchase`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      )
      alert("Purchase successful!")
      fetchSweets()
    } catch {
      alert("Purchase failed (possibly out of stock)")
    }
  }

  const getStockStatus = (quantity) => {
    if (quantity === 0)
      return <span style={{ color: '#e74c3c', fontWeight: 'bold' }}>Sold Out</span>

    if (quantity < 10)
      return <span style={{ color: '#e67e22', fontWeight: 'bold' }}>
        🔥 Hurry! Only {quantity} left!
      </span>

    return <span style={{ color: '#27ae60', fontWeight: 'bold' }}>
      ✅ In Stock
    </span>
  }

  const filteredSweets = sweets.filter(sweet => {
    if (!searchTerm) return true
    const term = searchTerm.toLowerCase()
    return (
      sweet.name.toLowerCase().includes(term) ||
      sweet.category.toLowerCase().includes(term)
    )
  })

  return (
    <div className="container">
      <div className="welcome-banner">
        <h1>Our Premium Sweets</h1>
        <p>Select from our exclusive collection of handcrafted delights.</p>
      </div>

      <div className="grid">
        {filteredSweets.map(sweet => (
          <div key={sweet.id} className="card">
            <div className="card-image-container">
              <img
                src={getSweetImage(sweet.name, sweet.category)}
                alt={sweet.name}
                className="sweet-image"
              />
            </div>

            <div className="card-content">
              <h3>{sweet.name}</h3>
              <span className="category-tag">{sweet.category}</span>

              <div className="price">₹{sweet.price.toFixed(2)}</div>

              <p style={{ fontSize: '0.9rem', color: '#666', marginTop: '10px' }}>
                {role === 'admin'
                  ? <span>Warehouse Stock: <strong>{sweet.quantity}</strong></span>
                  : getStockStatus(sweet.quantity)
                }
              </p>

              {role !== 'admin' && (
                <button
                  className="btn-buy"
                  onClick={() => handleBuy(sweet.id)}
                  disabled={sweet.quantity === 0}
                  style={{ marginTop: '15px' }}
                >
                  {sweet.quantity > 0 ? "Purchase" : "Out of Stock"}
                </button>
              )}
            </div>
          </div>
        ))}

        {filteredSweets.length === 0 && (
          <p style={{ gridColumn: '1 / -1', textAlign: 'center', color: '#888' }}>
            No sweets found matching "{searchTerm}"
          </p>
        )}
      </div>
    </div>
  )
}

export default SweetsList