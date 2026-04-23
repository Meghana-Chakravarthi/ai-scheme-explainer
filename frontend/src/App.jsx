import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { LanguageProvider } from './contexts/LanguageContext'
import Navbar from './components/Navbar'
import Footer from './components/Footer'
import Home from './pages/Home'
import Results from './pages/Results'
import Compare from './pages/Compare'
import Explore from './pages/Explore'
import Eligibility from './pages/Eligibility'

function App() {
  return (
    <LanguageProvider>
      <Router>
        <div className="min-h-screen flex flex-col">
          <Navbar />
          <main className="flex-grow">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/explore" element={<Explore />} />
              <Route path="/results" element={<Results />} />
              <Route path="/scheme/:name" element={<Results />} />
              <Route path="/compare" element={<Compare />} />
              <Route path="/eligibility" element={<Eligibility />} />
            </Routes>
          </main>
          <Footer />
        </div>
      </Router>
    </LanguageProvider>
  )
}

export default App
