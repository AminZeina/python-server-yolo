import { useEffect, useRef, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const baseUrl = useRef("http://localhost:8080")
  const [latestImageUrl, setLatestImageUrl] = useState("http://localhost:8080/latest-image")
  const [isRefreshing, setIsRefreshing] = useState(false);
  const refreshIntervalId = useRef(null);

  const toggleRefreshing = () => {
    setIsRefreshing((prev) => !prev);
  }

  useEffect(() => {
    if (isRefreshing) {
      refreshIntervalId.current = setInterval(() => {setLatestImageUrl(baseUrl.current + "/latest-image?" + new Date().getTime())}, 2000); 
    } else {
      clearInterval(refreshIntervalId.current);
    }
    }, [isRefreshing]);


  return (
    <>
      <div>
      <h1>Drone Image Viewer</h1>
      <div>
        <button
          id="toggleRefreshButton"
          onClick={toggleRefreshing}
          className="refresh-button"
        >
          {isRefreshing ? "Stop refreshing image" : "Start refreshing image"}
        </button>
      </div>
      <div>
        <img
          id="droneImage"
          src={latestImageUrl}
          alt="Drone Feed"
          className="drone-image"
        />
      </div>
    </div>
    </>
  )
}

export default App
