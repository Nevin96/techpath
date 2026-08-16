interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
}

function SearchBar({
  value,
  onChange,
  onSubmit,
}: SearchBarProps) {
  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    onSubmit();
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="mx-auto flex max-w-2xl items-center gap-3 rounded-2xl border border-slate-200 bg-white p-2 shadow-sm transition focus-within:border-indigo-400 focus-within:ring-4 focus-within:ring-indigo-50"
    >
      <span className="pl-3 text-lg text-slate-400">
        🔍
      </span>

      <input
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder="Search a skill..."
        className="min-w-0 flex-1 bg-transparent px-2 py-3 text-slate-900 outline-none placeholder:text-slate-400"
      />

      <button
        type="submit"
        className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-medium text-white transition hover:bg-slate-700"
      >
        Explore
      </button>
    </form>
  );
}

export default SearchBar;