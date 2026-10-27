import { Mail, Phone, MapPin } from 'lucide-react';

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-primary text-white mt-12">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand */}
          <div>
            <h3 className="text-2xl font-bold text-accent mb-4">TimeX</h3>
            <p className="text-gray-400">
              Premium luxury watches for every occasion. Experience timeless elegance.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-bold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/products" className="hover:text-accent transition">Shop</a></li>
              <li><a href="/" className="hover:text-accent transition">About Us</a></li>
              <li><a href="/" className="hover:text-accent transition">Contact</a></li>
              <li><a href="/" className="hover:text-accent transition">FAQ</a></li>
            </ul>
          </div>

          {/* Support */}
          <div>
            <h4 className="font-bold mb-4">Support</h4>
            <ul className="space-y-2 text-gray-400">
              <li><a href="/" className="hover:text-accent transition">Returns</a></li>
              <li><a href="/" className="hover:text-accent transition">Shipping</a></li>
              <li><a href="/" className="hover:text-accent transition">Warranty</a></li>
              <li><a href="/" className="hover:text-accent transition">Track Order</a></li>
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-bold mb-4">Contact Us</h4>
            <div className="space-y-3 text-gray-400">
              <div className="flex items-center space-x-2">
                <Phone size={16} />
                <span>+1 (555) 123-4567</span>
              </div>
              <div className="flex items-center space-x-2">
                <Mail size={16} />
                <span>support@timex.com</span>
              </div>
              <div className="flex items-center space-x-2">
                <MapPin size={16} />
                <span>123 Luxury Ave, NY 10001</span>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom */}
        <div className="border-t border-gray-700 pt-8">
          <div className="flex flex-col md:flex-row justify-between items-center text-gray-400 text-sm">
            <p>&copy; {currentYear} TimeX. All rights reserved.</p>
            <div className="flex space-x-6 mt-4 md:mt-0">
              <a href="/" className="hover:text-accent transition">Privacy Policy</a>
              <a href="/" className="hover:text-accent transition">Terms of Service</a>
              <a href="/" className="hover:text-accent transition">Cookie Policy</a>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
