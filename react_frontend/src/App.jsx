import Hello from "./components/Hello";
import Gig from "./components/Gig";
import GigList from "./components/GigList";
import makersLogo from "./assets/Makers-Logo.png";
import "./App.css";



function App() {
  return (
    <>
      <Hello name="World" />
      <img className="logo" src={makersLogo}></img>
      <GigList />

    </>
  );
}

export default App;
