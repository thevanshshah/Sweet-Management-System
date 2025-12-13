import { useState } from 'react'
import axios from 'axios'

function Register({ onLoginClick }) {
  const [formData, setFormData] = useState({
    username: '',
    password: '',
    role: 'customer' // Default role
  })
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value})
  }

  const handleRegister = async (e) => {
    e.preventDefault()
    setError('')
    setSuccess('')

    try {
      await axios.post('http://127.0.0.1:8000/api/auth/register', formData)
      setSuccess('Registration successful! Please log in.')
      // Optional: Clear form
      setFormData({ username: '', password: '', role: 'customer' })
    } catch (err) {
      console.error(err)
      if (err.response && err.response.data.detail) {
        setError(err.response.data.detail)
      } else {
        setError('Registration failed. Username might be taken.')
      }
    }
  }

  return (
    <div className="card" style={{ maxWidth: '400px', margin: '0 auto', padding: '30px' }}>
      <h2 style={{textAlign: 'center', color: '#2c3e50'}}>Sign Up</h2>
      
      {success ? (
        <div style={{textAlign: 'center'}}>
          <p style={{color: 'green', fontWeight: 'bold'}}>{success}</p>
          <button 
            className="btn-buy" 
            onClick={onLoginClick}
            style={{marginTop: '15px'}}
          >
            Go to Login
          </button>
        </div>
      ) : (
        <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          
          <div>
            <label style={{fontWeight: 'bold', fontSize: '0.9rem'}}>Username</label>
            <input 
              type="text" 
              name="username"
              value={formData.username}
              onChange={handleChange}
              style={inputStyle}
              required
            />
          </div>

          <div>
            <label style={{fontWeight: 'bold', fontSize: '0.9rem'}}>Password</label>
            <input 
              type="password" 
              name="password"
              value={formData.password}
              onChange={handleChange}
              style={inputStyle}
              required
            />
          </div>

          <div>
            <label style={{fontWeight: 'bold', fontSize: '0.9rem'}}>Role</label>
            <select 
              name="role" 
              value={formData.role} 
              onChange={handleChange}
              style={inputStyle}
            >
              <option value="customer">Customer (Buyer)</option>
              <option value="admin">Admin (Seller)</option>
            </select>
          </div>

          <button type="submit" className="btn-buy" style={{marginTop: '10px'}}>
            Create Account
          </button>
        </form>
      )}

      {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '15px' }}>{error}</p>}
      
      {!success && (
        <p style={{textAlign: 'center', marginTop: '20px', fontSize: '0.9rem'}}>
          Already have an account? <br/>
          <span 
            onClick={onLoginClick} 
            style={{color: '#3498db', cursor: 'pointer', fontWeight: 'bold'}}
          >
            Log in here
          </span>
        </p>
      )}
    </div>
  )
}

const inputStyle = {
  width: '100%',
  padding: '10px',
  borderRadius: '5px',
  border: '1px solid #ccc',
  marginTop: '5px'
}

export default Register