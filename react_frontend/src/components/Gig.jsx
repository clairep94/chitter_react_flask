import { useState } from 'react';

function Gig(props) {
    const [liked, setLike] = useState(false);

    const options = {
        timeZone: 'Europe/London',
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric',
        second: 'numeric',
    };

    const dateTimeString = props.data.time;
    const dateTimeObject = new Date(dateTimeString);
    const dateFormatted = dateTimeObject.toLocaleString('en-GB', options);

    const like = () => {
        setLike((prevState) => !prevState);
        console.log("liked");
        console.log(liked);
    };

    return (
        <>
        <div className={`gig-box ${liked ? 'liked' : ''}`}>
            <h3 className="gig-band-name">{props.data.band_name}</h3>
            {props.data.image_url && <img src={props.data.image_url} alt={props.data.band_name} className="gig-band-image" />}
            <p className="gig-description">{props.data.description}</p>
            <p className="gig-date">{dateFormatted}</p>
            <p className="gig-location">{props.data.location}</p>
            <button className={`like-button ${liked ? 'liked' : ''}`} onClick={like}>
            Like
            </button>
        </div>
        </>
    );
}

export default Gig;
