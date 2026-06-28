function Card({ children, className = "" }) {
  return (
    <div
      className={`bg-white rounded-xl shadow-md border border-gray-200 p-6 mb-6 ${className}`}
    >
      {children}
    </div>
  );
}

export default Card;