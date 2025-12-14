import { useState, useEffect } from 'react'
import axios from 'axios'
import './App.css'
import SweetsList from './components/SweetsList'
import Login from './components/Login'
import AdminPanel from './components/AdminPanel'
import Register from './components/Register'
import { FaStore } from 'react-icons/fa'   // ✅ Storefront icon

function App() {
  const [message, setMessage] = useState('')
  const [token, setToken] = useState(null)
  const [role, setRole] = useState(null)
  const [view, setView] = useState('shop')
  const [searchTerm, setSearchTerm] = useState('')
  const [authView, setAuthView] = useState('login')

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/')
      .then(res => setMessage(res.data.message))
      .catch(() => setMessage('Backend Disconnected'))
  }, [])

  const handleLogout = () => {
    setToken(null)
    setRole(null)
    setView('shop')
    setAuthView('login')
  }

  return (
    <div>
      {/* NAVBAR */}
      <nav className="navbar">
        {/* LOGO */}
        <div
          className="logo"
          onClick={() => setView('shop')}
          style={{
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            fontWeight: '700',
            fontSize: '1.3rem'
          }}
        >
          <FaStore size={22} color="#fff" />
          <span>Sweet Shop </span>
        </div>

        {/* SEARCH */}
        {view === 'shop' && (
          <div className="search-bar">
            <input
              type="text"
              placeholder="Search sweets..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={searchStyle}
            />
          </div>
        )}

        {/* NAV LINKS */}
        <div className="nav-links">
          {!token ? (
            <span style={{ fontSize: '0.9rem' }}>Guest Mode</span>
          ) : (
            <div style={{ display: 'flex', gap: '15px', alignItems: 'center' }}>
              <span style={{ fontSize: '0.8rem', marginRight: '10px' }}>
                Logged in as: <strong>{role?.toUpperCase()}</strong>
              </span>

              <button onClick={() => setView('shop')}>Shop</button>

              {role === 'admin' && (
                <button
                  onClick={() => setView('admin')}
                  style={{ backgroundColor: '#e74c3c', border: 'none' }}
                >
                  Admin Panel
                </button>
              )}

              <button onClick={handleLogout}>Logout</button>
            </div>
          )}
        </div>
      </nav>

      {/* MAIN CONTENT */}
      {!token ? (
        <div className="container">
          <div className="welcome-banner">
            <h1>Welcome to Sweet Manager</h1>
            <p>Please log in or register to browse our exclusive sweets.</p>
          </div>

          {authView === 'login' ? (
            <Login
              setToken={setToken}
              setRole={setRole}
              onRegisterClick={() => setAuthView('register')}
            />
          ) : (
            <Register onLoginClick={() => setAuthView('login')} />
          )}
        </div>
      ) : (
        <>
          {view === 'shop' && (
            <SweetsList
              token={token}
              searchTerm={searchTerm}
              role={role}
            />
          )}

          {/* SECURITY: render admin panel only if admin */}
          {view === 'admin' && role === 'admin' && (
            <AdminPanel token={token} />
          )}
        </>
      )}

      {/* FOOTER */}
      <footer
        style={{
          textAlign: 'center',
          marginTop: '50px',
          color: '#aaa',
          fontSize: '0.8rem'
        }}
      >
        System Status: {message}
      </footer>
    </div>
  )
}

const searchStyle = {
  padding: '8px 15px',
  borderRadius: '20px',
  border: 'none',
  width: '250px',
  outline: 'none',
  fontSize: '0.9rem',
  color: '#333'
}

export default App