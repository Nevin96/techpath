function Navbar() {
  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <div className="text-xl font-bold tracking-tight">
          Tech<span className="text-indigo-600">Path</span>
        </div>

        <div className="flex items-center gap-6 text-sm text-slate-600">
          <a
            href="#"
            className="font-medium text-slate-900"
          >
            Explore
          </a>

          <a
            href="#"
            className="transition hover:text-slate-900"
          >
            About
          </a>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;