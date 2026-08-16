import { BrowserRouter, Routes, Route } from "react-router-dom";

import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import SkillPage from "./pages/SkillPage";
import GraphPage from "./pages/GraphPage";


function App() {
  return (
    <BrowserRouter>

      <Navbar />

      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/skills/:skillName"
          element={<SkillPage />}
        />
        <Route
          path="/skills/:skillName/graph"
          element={<GraphPage />}
        />
      </Routes>

    </BrowserRouter>
  );
}


export default App;