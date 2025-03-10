import { useEffect, useRef, useState } from 'react'
import './App.css'
import './index.css'

function App() {
  const baseUrl = useRef("http://localhost:8080")
  const [latestImageUrl, setLatestImageUrl] = useState(baseUrl.current + "/latest-image")
  const [latestConfidence, setLatestConfidence] = useState(0.0)
  const [isRefreshing, setIsRefreshing] = useState(false);
  const refreshIntervalId = useRef(null);

  const toggleRefreshing = () => {
    setIsRefreshing((prev) => !prev);
  }

  const getLatestImage = () => {
    fetch(baseUrl.current + "/latest-image?" + new Date().getTime(), {
      method: "GET",
    }).then((response) => {
      if (response.ok) {
        return response.json()
      }
    }).then((data) => {
      setLatestImageUrl(data.img_url._url)
      setLatestConfidence(data.confidence) 
    })
  }

  const fireHandler = () => {
    
    fetch(baseUrl.current + "/fire", {
      method: "POST",
    })
  }

  const fireColour = () => {
    if (latestConfidence < 0.25) return 'cyan'
    else if (latestConfidence < 0.50) return 'green'
    else if (latestConfidence < 0.75) return 'orange'
    else return 'red'
  }

  useEffect(() => {
    if (isRefreshing) {
      refreshIntervalId.current = setInterval(getLatestImage, 2000); 
    } else {
      clearInterval(refreshIntervalId.current);
    }
    }, [isRefreshing]);


  return (
    <>
      <h1>Drone Image Viewer</h1>
      <div>
        <button id="toggleRefreshButton" onClick={toggleRefreshing} style={{backgroundColor: 'cyan', marginBottom: "1em"}}>
          {isRefreshing ? "Stop refreshing image" : "Start refreshing image"}
        </button>
        <button id="fireButton" onClick={fireHandler} disabled={!isRefreshing} style={{backgroundColor: fireColour(), marginLeft: "1em"}}>
          Fire
        </button>
      </div>
      <div>
        <img id="droneImage" src={latestImageUrl} alt="Drone Feed" style={{width:"75%", height:"auto", shadowColor: fireColour}}/>
      </div>      
    </>
  )
}

export default App
