import { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiClient } from '@/services/api';
import { useCartStore } from '@/store/cartStore';
import { useAuthStore } from '@/store/authStore';
import type { Product, Review } from '@/types';
import { Star, ShoppingCart, Heart } from 'lucide-react';

export default function ProductDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthStore();
  const [product, setProduct] = useState<Product | null>(null);
  const [reviews, setReviews] = useState<Review[]>([]);
  const [quantity, setQuantity] = useState(1);
  const [loading, setLoading] = useState(true);
  const [inWishlist, setInWishlist] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        if (id) {
          const productResponse = await apiClient.getProductById(id);
          setProduct(productResponse.data);

          const reviewsResponse = await apiClient.getProductReviews(id);
          setReviews(reviewsResponse.data);
        }
      } catch (error) {
        console.error('Failed to fetch product:', error);
        navigate('/products');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [id, navigate]);

  const handleAddToCart = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      if (id) {
        await apiClient.addToCart(id, quantity);
        alert('Added to cart!');
      }
    } catch (error) {
      console.error('Failed to add to cart:', error);
    }
  };

  const handleToggleWishlist = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      if (id) {
        if (inWishlist) {
          await apiClient.removeFromWishlist(id);
        } else {
          await apiClient.addToWishlist(id);
        }
        setInWishlist(!inWishlist);
      }
    } catch (error) {
      console.error('Failed to update wishlist:', error);
    }
  };

  if (loading) {
    return <div className="container mx-auto px-4 py-8 text-center">Loading...</div>;
  }

  if (!product) {
    return <div className="container mx-auto px-4 py-8 text-center">Product not found</div>;
  }

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        {/* Image */}
        <div className="bg-gray-100 rounded-lg overflow-hidden">
          {product.imageUrl ? (
            <img
              src={product.imageUrl}
              alt={product.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="w-full h-96 flex items-center justify-center text-gray-400">
              No image available
            </div>
          )}
        </div>

        {/* Details */}
        <div>
          <h1 className="text-3xl font-bold mb-2">{product.name}</h1>
          <p className="text-xl text-gray-600 mb-4">{product.brand}</p>

          {/* Rating */}
          <div className="flex items-center mb-6">
            <div className="flex text-yellow-400">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  size={20}
                  fill={i < Math.round(product.averageRating) ? 'currentColor' : 'none'}
                />
              ))}
            </div>
            <span className="text-gray-600 ml-2">
              {product.averageRating} ({product.totalReviews} reviews)
            </span>
          </div>

          {/* Price */}
          <div className="mb-6">
            {product.discountPrice ? (
              <>
                <p className="text-sm text-gray-500 line-through mb-2">
                  ${product.price}
                </p>
                <p className="text-4xl font-bold text-accent">
                  ${product.discountPrice}
                </p>
              </>
            ) : (
              <p className="text-4xl font-bold">${product.price}</p>
            )}
          </div>

          {/* Description */}
          <p className="text-gray-700 mb-6">{product.description}</p>

          {/* Specifications */}
          <div className="mb-6 p-4 bg-gray-100 rounded-lg">
            <h3 className="font-bold mb-3">Specifications</h3>
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Model</p>
                <p className="font-semibold">{product.model}</p>
              </div>
              <div>
                <p className="text-gray-600">Brand</p>
                <p className="font-semibold">{product.brand}</p>
              </div>
              <div>
                <p className="text-gray-600">Material</p>
                <p className="font-semibold">{product.material}</p>
              </div>
              <div>
                <p className="text-gray-600">Water Resistance</p>
                <p className="font-semibold">{product.waterResistance}</p>
              </div>
              <div>
                <p className="text-gray-600">Movement</p>
                <p className="font-semibold">{product.movement}</p>
              </div>
              <div>
                <p className="text-gray-600">Diameter</p>
                <p className="font-semibold">{product.diameter}</p>
              </div>
            </div>
          </div>

          {/* Quantity and Add to Cart */}
          <div className="flex gap-4 mb-6">
            <div className="flex items-center border border-gray-300 rounded-lg">
              <button
                onClick={() => setQuantity(Math.max(1, quantity - 1))}
                className="px-4 py-2"
              >
                -
              </button>
              <input
                type="number"
                value={quantity}
                onChange={(e) => setQuantity(Math.max(1, parseInt(e.target.value) || 1))}
                className="w-12 text-center border-l border-r border-gray-300"
              />
              <button
                onClick={() => setQuantity(quantity + 1)}
                className="px-4 py-2"
              >
                +
              </button>
            </div>
            <button
              onClick={handleAddToCart}
              className="btn-primary flex-1 flex items-center justify-center gap-2"
            >
              <ShoppingCart size={20} />
              Add to Cart
            </button>
            <button
              onClick={handleToggleWishlist}
              className={`px-4 py-2 rounded-lg transition ${
                inWishlist
                  ? 'bg-accent text-white'
                  : 'bg-gray-200 text-primary hover:bg-gray-300'
              }`}
            >
              <Heart size={20} fill={inWishlist ? 'currentColor' : 'none'} />
            </button>
          </div>
        </div>
      </div>

      {/* Reviews Section */}
      <div className="mb-12">
        <h2 className="text-2xl font-bold mb-6">Customer Reviews</h2>
        {reviews.length === 0 ? (
          <p className="text-gray-500">No reviews yet</p>
        ) : (
          <div className="space-y-4">
            {reviews.map((review) => (
              <div key={review.id} className="border border-gray-200 rounded-lg p-4">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <p className="font-bold">{review.userName}</p>
                    <div className="flex text-yellow-400">
                      {[...Array(5)].map((_, i) => (
                        <Star
                          key={i}
                          size={16}
                          fill={i < review.rating ? 'currentColor' : 'none'}
                        />
                      ))}
                    </div>
                  </div>
                  <p className="text-gray-600 text-sm">
                    {new Date(review.createdAt).toLocaleDateString()}
                  </p>
                </div>
                <h4 className="font-semibold mb-2">{review.title}</h4>
                <p className="text-gray-700">{review.comment}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
