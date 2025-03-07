import { render, screen } from "@testing-library/react";
import HelloWorld from "../HelloWorld";

test("renders the Hello, World! message", () => {
  render(<HelloWorld />);
  expect(screen.getByText("Hello, World!")).toBeInTheDocument();
});
