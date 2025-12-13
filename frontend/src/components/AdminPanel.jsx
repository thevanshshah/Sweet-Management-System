import { useState, useEffect } from 'react'
import axios from 'axios'

function AdminPanel({ token }) {
  // Form State
  const [formData, setFormData] = useState({ name: '', category: '', price: '', quantity: '' })
  
  // List State
  const [sweets, setSweets] = useState([])
  const [message, setMessage] = useState('')

  // 1. Fetch Sweets for Management List
  const fetchSweets = async () => {
    try {
      const res = await axios.get('http://127.0.0.1:8000/api/sweets')
      setSweets(res.data)
    } catch (err) {
      console.error("Failed to fetch sweets")
    }
  }

  useEffect(() => { fetchSweets() }, [])

  // 2. Add Sweet
  const handleAdd = async (e) => {
    e.preventDefault()
    try {
      await axios.post('http://127.0.0.1:8000/api/sweets', formData, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMessage(`✅ Added ${formData.name}`)
      setFormData({ name: '', category: '', price: '', quantity: '' })
      fetchSweets()
    } catch (err) {
      setMessage("❌ Failed to add sweet")
    }
  }

  // 3. Delete Sweet
  const handleDelete = async (id) => {
    if(!confirm("Are you sure you want to delete this item?")) return
    try {
      await axios.delete(`http://127.0.0.1:8000/api/sweets/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMessage("🗑️ Item deleted")
      fetchSweets()
    } catch (err) {
      alert("Failed to delete")
    }
  }

  // 4. Restock Sweet (+10)
  const handleRestock = async (id) => {
    try {
      await axios.post(`http://127.0.0.1:8000/api/sweets/${id}/restock?amount=10`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      setMessage("📦 Stock added (+10)")
      fetchSweets()
    } catch (err) {
      alert("Failed to restock")
    }
  }

  return (
    <div className="container">
      <h2 style={{color: '#c0392b', textAlign: 'center'}}>🛡️ Admin Dashboard</h2>
      {message && <div style={msgStyle}>{message}</div>}

      {/* --- ADD NEW SWEET FORM --- */}
      <div className="card" style={{padding: '20px', marginBottom: '40px', borderTop: '4px solid #c0392b'}}>
        <h3>Add New Inventory</h3>
        <form onSubmit={handleAdd} style={{display: 'flex', gap: '10px', flexWrap: 'wrap'}}>
          <input style={inputStyle} placeholder="Name" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} required />
          <input style={inputStyle} placeholder="Category" value={formData.category} onChange={e => setFormData({...formData, category: e.target.value})} required />
          <input style={inputStyle} type="number" placeholder="Price (₹)" value={formData.price} onChange={e => setFormData({...formData, price: e.target.value})} required />
          <input style={inputStyle} type="number" placeholder="Qty" value={formData.quantity} onChange={e => setFormData({...formData, quantity: e.target.value})} required />
          <button type="submit" className="btn-buy" style={{backgroundColor: '#27ae60'}}>+ Add</button>
        </form>
      </div>

      {/* --- MANAGE EXISTING SWEETS --- */}
      <h3>Manage Stock</h3>
      <div style={{display: 'flex', flexDirection: 'column', gap: '10px'}}>
        {sweets.map(sweet => (
          <div key={sweet.id} style={rowStyle}>
            <div style={{flex: 2}}>
              <strong>{sweet.name}</strong> <span style={{fontSize:'0.8rem', color:'#7f8c8d'}}>({sweet.category})</span>
            </div>
            <div style={{flex: 1}}>₹{sweet.price}</div>
            <div style={{flex: 1}}>
              Stock: <strong>{sweet.quantity}</strong>
            </div>
            <div style={{flex: 1, display: 'flex', gap: '10px'}}>
              <button onClick={() => handleRestock(sweet.id)} style={btnRestock}>+ Restock</button>
              <button onClick={() => handleDelete(sweet.id)} style={btnDelete}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

// Styles
const msgStyle = { backgroundColor: '#fadbd8', color: '#c0392b', padding: '10px', borderRadius: '5px', marginBottom: '20px', textAlign: 'center' }
const inputStyle = { padding: '8px', borderRadius: '4px', border: '1px solid #ddd', flex: 1, minWidth: '100px' }
const rowStyle = { display: 'flex', alignItems: 'center', backgroundColor: 'white', padding: '15px', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }
const btnRestock = { backgroundColor: '#f39c12', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer' }
const btnDelete = { backgroundColor: '#e74c3c', color: 'white', border: 'none', padding: '5px 10px', borderRadius: '4px', cursor: 'pointer' }

export default AdminPanel