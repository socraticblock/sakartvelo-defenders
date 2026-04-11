import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import About from './pages/About'
import Gameplay from './pages/Gameplay'

function App() {
  return (
    <>
      <Navbar />
      <main style={{ paddingTop: '70px' }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/gameplay" element={<Gameplay />} />
        </Routes>
      </main>
      <Footer />
    </>
  )
}

export default App
