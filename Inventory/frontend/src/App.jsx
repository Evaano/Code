import "@mantine/core/styles.css";
import { MantineProvider } from "@mantine/core";
import Home from "./components/Home";

export default function App() {
  return (
    <MantineProvider>
      <Home />
    </MantineProvider>
  );
}
