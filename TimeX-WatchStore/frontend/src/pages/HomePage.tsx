import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { apiClient } from '@/services/api';
import type { Product } from '@/types';
import { Star, ShoppingCart } from 'lucide-react';

export default function HomePage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const response = await apiClient.getProducts();
        setProducts(response.data.slice(0, 6));
      } catch (error) {
        console.error('Failed to fetch products:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-primary to-secondary text-white py-20">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-5xl font-bold mb-4">Welcome to TimeX</h1>
          <p className="text-xl mb-8">Discover premium luxury watches for every occasion</p>
          <Link to="/products" className="btn-primary inline-block">
            Shop Now
          </Link>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold mb-12 text-center">Featured Watches</h2>
          
          {loading ? (
            <div className="text-center py-12">
              <p className="text-gray-500">Loading products...</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {products.map((product) => (
                <div
                  key={product.id}
                  className="bg-white rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition"
                >
                  {product.imageUrl && (
                    <img
                      src={product.imageUrl}
                      alt={product.name}
                      className="w-full h-48 object-cover"
                    />
                  )}
                  <div className="p-6">
                    <h3 className="text-xl font-bold mb-2">{product.name}</h3>
                    <p className="text-gray-600 text-sm mb-4">{product.brand}</p>
                    <div className="flex items-center mb-4">
                      <div className="flex text-yellow-400">
                        {[...Array(5)].map((_, i) => (
                          <Star
                            key={i}
                            size={16}
                            fill={i < Math.round(product.averageRating) ? 'currentColor' : 'none'}
                          />
                        ))}
                      </div>
                      <span className="text-gray-600 text-sm ml-2">
                        ({product.totalReviews})
                      </span>
                    </div>
                    <div className="flex justify-between items-center">
                      <div>
                        {product.discountPrice ? (
                          <>
                            <p className="text-sm text-gray-500 line-through">
                              ${product.price}
                            </p>
                            <p className="text-2xl font-bold text-accent">
                              ${product.discountPrice}
                            </p>
                          </>
                        ) : (
                          <p className="text-2xl font-bold">${product.price}</p>
                        )}
                      </div>
                      <Link
                        to={`/products/${product.id}`}
                        className="btn-primary flex items-center space-x-2"
                      >
                        <ShoppingCart size={18} />
                      </Link>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-gray-100 py-16">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="text-4xl font-bold text-secondary mb-2">100%</div>
              <p className="text-gray-600">Authentic Products</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-secondary mb-2">Free</div>
              <p className="text-gray-600">Worldwide Shipping</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-secondary mb-2">24/7</div>
              <p className="text-gray-600">Customer Support</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
