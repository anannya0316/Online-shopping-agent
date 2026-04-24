export default function ProductCard({ product }) {
  const filled = Math.round(product.rating)

  return (
    <div className="product-card">
      <div className="product-header">
        <span className="best-pick">Best Pick</span>
        <span className={`source-badge source-${product.source}`}>{product.source}</span>
      </div>

      <h2 className="product-title">{product.title}</h2>

      <div className="product-meta">
        <span className="price">${product.price.toFixed(2)}</span>
        {product.rating > 0 && (
          <span className="rating">
            {'★'.repeat(filled)}{'☆'.repeat(5 - filled)} {product.rating.toFixed(1)}
          </span>
        )}
      </div>

      {product.link && (
        <a href={product.link} target="_blank" rel="noopener noreferrer" className="view-btn">
          View Product →
        </a>
      )}
    </div>
  )
}
