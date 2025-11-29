import React,{ useState, useEffect } from 'react'

function App() {
    
    const [data, setData] = useState([{}])

    useEffect(() => {
        fetch("/recommendations.html").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])
  return (
    <div>
        {(typeof data.recommendations ==='undefined')?(
            <p>Loading...</p>
        ) : (
            data.irecommendations.map((recommendations, i) => (
                <p key={i}>{recommendations}</p>
            ))
        )}
        
    </div>
  )
}

export default App
