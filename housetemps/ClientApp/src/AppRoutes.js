import { FetchData } from "./components/FetchData";
import { Home } from "./components/Home";

const AppRoutes = [
  {
    index: true,
    element: <Home />,
  },
  {
    path: "/temperature",
    element: <FetchData />,
  },
];

export default AppRoutes;
