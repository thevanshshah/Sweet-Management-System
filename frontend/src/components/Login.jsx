import { useState } from 'react'
import axios from 'axios'

// 1. Add onRegisterClick to props
function Login({ setToken, setRole, onRegisterClick }) { 
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')

    const params = new URLSearchParams()
    params.append('username', username)
    params.append('password', password)

    try {
      const response = await axios.post('http://127.0.0.1:8000/api/auth/login', params)
      setToken(response.data.access_token)
      setRole(response.data.role)
    } catch (err) {
      console.error(err)
      setError('Invalid credentials')
    }
  }

  return (
    <div className="card" style={{ maxWidth: '400px', margin: '0 auto', padding: '30px' }}>
      <h2 style={{textAlign: 'center', color: '#2c3e50'}}>Login</h2>
      <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <input 
          type="text" 
          placeholder="Username" 
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{padding: '10px', borderRadius: '5px', border: '1px solid #ccc'}}
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{padding: '10px', borderRadius: '5px', border: '1px solid #ccc'}}
        />
        <button type="submit" className="btn-buy" style={{marginTop: '10px'}}>Log In</button>
      </form>
      {error && <p style={{ color: 'red', textAlign: 'center', marginTop: '10px' }}>{error}</p>}
      
      {/* 2. Add the "Switch to Register" link */}
      <p style={{textAlign: 'center', marginTop: '20px', fontSize: '0.9rem'}}>
        New to Sweet Manager? <br/>
        <span 
          onClick={onRegisterClick} 
          style={{color: '#3498db', cursor: 'pointer', fontWeight: 'bold'}}
        >
          Create an account
        </span>
      </p>
    </div>
  )
}

export default Login