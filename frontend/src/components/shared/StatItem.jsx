function StatItem({ label, value }) {
  return (
    <div className="flex justify-between py-2 border-b">
      <span>{label}</span>

      <span className="font-semibold">
        {value}
      </span>
    </div>
  );
}

export default StatItem;