import { useEffect, useState } from "react";

function App() {
 const [msg, setMsg] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/hello")
      .then(res => res.json())
      .then(data => setMsg(data.message));
  }, []);

  return (
    <div>
      <h1>{ msg ? msg : "Loading..." }</h1>
    </div>
  );
}

export default App;
