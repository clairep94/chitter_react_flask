import { useState, useEffect } from "react";
import Gig from "./Gig";

function GigList() {
    const [gigs, setGigs] = useState([]);
    const [showFavourites, setShowFavourites] = useState(false);

    useEffect(() => {
        const URL = 'http://127.0.0.1:5000/posts';
      
        fetch(URL)
          .then((res) => res.json())
          .then((data) => setGigs(data))
          .catch(error => {
            console.error('Fetch error:', error);
          });
      }, []);

    const handleShowFavourites = () => {
        setShowFavourites((prevShowFavourites) => !prevShowFavourites);
    };

    // const filteredGigs = showFavourites ? gigs.filter(gig => gig.liked) : gigs;

    if (showFavourites === false) {
        return (
            <>
            <h1>Gigs in Town:</h1>
            <button className={`show-favourites-button ${showFavourites? "favourites": ''}`} onClick={handleShowFavourites}>
                {showFavourites ? "Show All" : "Show Favourites"}
            </button>
            <div className="gigs">
                {gigs.map((gigData) => (
                <Gig key={gigData.event_id} data={gigData} />
                ))}
            </div>
            </>
        )
    } else {
        return (
            <>
            <h1>Gigs in Town:</h1>
            <button className={`show-favourites-button ${showFavourites? "favourites": ''}`} onClick={handleShowFavourites}>
                {showFavourites ? "Show All" : "Show Favourites"}
            </button>
            <div className="gigs">
                {gigs
                .map(filteredGigData => (
                    <Gig key={filteredGigData.event_id} data={filteredGigData} />
                    )
                .filter(gigComponent => gigComponent.liked)    
                    )}
            </div>
            </>
        );
    
    }
}

export default GigList;
