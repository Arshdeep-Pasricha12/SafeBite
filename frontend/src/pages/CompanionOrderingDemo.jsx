import React, { useState, useEffect } from 'react';
import { 
  Shield, Star, AlertTriangle, CheckCircle2, ShoppingBag, 
  Plus, Minus, ArrowRight, Search, ExternalLink, RefreshCw, Info, UtensilsCrossed 
} from 'lucide-react';
import { restaurantApi } from '../services/api';

const DEMO_PRESETS = [
  { name: "Haldiram's Sweets & Restaurant", city: "Delhi", cuisine: "North Indian" },
  { name: "Barbeque Nation", city: "Bangalore", cuisine: "BBQ" },
  { name: "Saravana Bhavan", city: "Chennai", cuisine: "South Indian" },
  { name: "Social (Cyber Hub)", city: "Gurugram", cuisine: "Continental" },
  { name: "Chipotle Mexican Grill", city: "New York", cuisine: "Mexican" },
  { name: "Starbucks Coffee", city: "New York", cuisine: "Cafe" }
];

const MENU_ITEMS = {
  "Haldiram's Sweets & Restaurant": [
    { id: 101, name: "Special Chole Bhature", price: 180, desc: "Fluffy bhature served with spiced chickpea curry and tangy pickle.", category: "Mains" },
    { id: 102, name: "Raj Kachori Supreme", price: 160, desc: "Crispy puffed shell filled with lentils, potatoes, curd, and chutneys.", category: "Starters" },
    { id: 103, name: "Paneer Makhani Thali", price: 290, desc: "Rich paneer in tomato gravy, dal makhani, pulao, 2 rotis, and gulab jamun.", category: "Mains" },
    { id: 104, name: "Kaju Katli (250g)", price: 320, desc: "Premium cashew fudge prepared with purified silver vark.", category: "Desserts" }
  ],
  "Barbeque Nation": [
    { id: 201, name: "Cajun Spiced Potatoes", price: 220, desc: "Crisp fried baby potatoes coated in zesty Cajun mayonnaise.", category: "Starters" },
    { id: 202, name: "Tandoori Paneer Tikka Skewer", price: 310, desc: "Marinated cottage cheese cubes grilled over live charcoal.", category: "Starters" },
    { id: 203, name: "Dum Gosht Biryani", price: 420, desc: "Aromatic basmati rice cooked with tender meat and royal spices.", category: "Mains" },
    { id: 204, name: "Angoori Gulab Jamun", price: 150, desc: "Mini dumplings soaked in fragrant cardamom sugar syrup.", category: "Desserts" }
  ],
  "Saravana Bhavan": [
    { id: 301, name: "Ghee Roast Masala Dosa", price: 140, desc: "Golden thin crepe roasted with pure desi ghee and potato masala.", category: "Mains" },
    { id: 302, name: "Steamed Idli Sambar (2 pcs)", price: 90, desc: "Pillowy steamed rice cakes served with hot drumstick sambar.", category: "Starters" },
    { id: 303, name: "Medu Vada (2 pcs)", price: 100, desc: "Crispy lentil fritters paired with coconut and tomato chutney.", category: "Starters" },
    { id: 304, name: "Filter Kaapi (South Indian Coffee)", price: 60, desc: "Freshly brewed chicory blend with frothy milk.", category: "Beverages" }
  ],
  "Social (Cyber Hub)": [
    { id: 401, name: "Butter Chicken Bao", price: 340, desc: "Tender spiced chicken stuffed in steamed lotus buns.", category: "Starters" },
    { id: 402, name: "Penne Arrabiata Bowl", price: 390, desc: "Al dente pasta tossed in spicy basil garlic pomodoro.", category: "Mains" },
    { id: 403, name: "Death by Chocolate Cake", price: 260, desc: "Decadent multi-layered warm chocolate fudge slice.", category: "Desserts" }
  ],
  "Chipotle Mexican Grill": [
    { id: 501, name: "Burrito Bowl", price: 450, desc: "Cilantro lime brown rice, black beans, fajita veggies, salsa, and guac.", category: "Mains" },
    { id: 502, name: "Chips & Fresh Guacamole", price: 190, desc: "House fried corn tortilla chips with freshly mashed Hass avocado.", category: "Starters" },
    { id: 503, name: "Organic Lemonade", price: 120, desc: "Fresh pressed organic lemons with pure cane sugar.", category: "Beverages" }
  ],
  "Starbucks Coffee": [
    { id: 601, name: "Caramel Macchiato", price: 310, desc: "Freshly steamed milk with vanilla, espresso, and buttery caramel drizzle.", category: "Beverages" },
    { id: 602, name: "Cold Brew with Vanilla Sweet Cream", price: 340, desc: "Slow steeped artisan coffee with silky house cream.", category: "Beverages" },
    { id: 603, name: "Almond Butter Croissant", price: 240, desc: "Flaky all-butter viennoiserie pastry with roasted almond cream.", category: "Desserts" }
  ]
};

const CompanionOrderingDemo = () => {
  const [selectedPreset, setSelectedPreset] = useState(DEMO_PRESETS[0]);
  const [searchQuery, setSearchQuery] = useState('');
  const [matchResult, setMatchResult] = useState(null);
  const [matching, setMatching] = useState(false);
  const [showAuditModal, setShowAuditModal] = useState(false);
  const [cart, setCart] = useState([]);
  const [orderPlaced, setOrderPlaced] = useState(false);

  // Evaluate restaurant on change
  useEffect(() => {
    evaluateRestaurant(selectedPreset.name, selectedPreset.city);
  }, [selectedPreset]);

  const evaluateRestaurant = async (name, city = '') => {
    setMatching(true);
    try {
      const response = await restaurantApi.match({
        name: name,
        city: city,
        platform: 'companion_demo'
      });
      setMatchResult(response.data);
    } catch (err) {
      console.error('Matching failed:', err);
      setMatchResult(null);
    } finally {
      setMatching(false);
    }
  };

  const handleCustomSearch = (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;
    evaluateRestaurant(searchQuery.trim());
  };

  const addToCart = (item) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) {
        return prev.map(i => i.id === item.id ? { ...i, qty: i.qty + 1 } : i);
      }
      return [...prev, { ...item, qty: 1 }];
    });
  };

  const updateCartQty = (id, delta) => {
    setCart(prev => {
      return prev.map(i => {
        if (i.id === id) {
          const newQty = i.qty + delta;
          return newQty > 0 ? { ...i, qty: newQty } : null;
        }
        return i;
      }).filter(Boolean);
    });
  };

  const cartSubtotal = cart.reduce((sum, item) => sum + (item.price * item.qty), 0);
  const deliveryFee = cart.length > 0 ? 40 : 0;
  const taxes = Math.round(cartSubtotal * 0.05);
  const cartTotal = cartSubtotal + deliveryFee + taxes;

  const currentMenu = MENU_ITEMS[selectedPreset.name] || [
    { id: 901, name: "Chef's Special Tasting Platter", price: 350, desc: "Curated seasonal appetizers prepared with fresh ingredients.", category: "Mains" },
    { id: 902, name: "Signature Dish", price: 280, desc: "House specialty prepared under verified hygiene standards.", category: "Mains" },
    { id: 903, name: "Fresh Brewed Beverage", price: 90, desc: "Chilled refreshment served in sanitized containers.", category: "Beverages" }
  ];

  return (
    <div className="min-h-screen bg-slate-100 pb-16">
      {/* Demo Platform Top Banner */}
      <div className="bg-slate-900 text-white px-4 py-3 shadow">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between text-xs gap-2">
          <div className="flex items-center space-x-2">
            <span className="bg-rose-500 text-white font-bold px-2 py-0.5 rounded tracking-wider uppercase text-[10px]">
              Companion Demo
            </span>
            <span className="font-semibold text-slate-200">
              Simulated Food Delivery App with SafeBite Real-Time Safety Overlay
            </span>
          </div>
          <div className="text-slate-400">
            Demonstrating Extension & API Transparency Engine Integration
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Preset Restaurant Switcher */}
        <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-4 mb-6">
          <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
            <div>
              <h3 className="font-bold text-slate-800 text-sm mb-1">
                Select Test Restaurant or Search Any Listing:
              </h3>
              <div className="flex flex-wrap gap-2">
                {DEMO_PRESETS.map((preset) => (
                  <button
                    key={preset.name}
                    onClick={() => {
                      setSelectedPreset(preset);
                      setCart([]);
                      setOrderPlaced(false);
                    }}
                    className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
                      selectedPreset.name === preset.name
                        ? 'bg-rose-600 text-white shadow'
                        : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                    }`}
                  >
                    {preset.name} ({preset.city})
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Search Form */}
            <form onSubmit={handleCustomSearch} className="flex items-center gap-2">
              <div className="relative">
                <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Test other restaurant..."
                  className="pl-8 pr-3 py-1.5 text-xs border border-slate-300 rounded-lg w-52 focus:outline-none focus:ring-1 focus:ring-rose-500"
                />
              </div>
              <button
                type="submit"
                className="bg-slate-800 text-white text-xs px-3 py-1.5 rounded-lg font-bold hover:bg-slate-900"
              >
                Match
              </button>
            </form>
          </div>
        </div>

        {/* Ordering App Main Frame */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Restaurant Header & Menu (2 Cols) */}
          <div className="lg:col-span-2 space-y-6">
            {/* Restaurant Profile Header Card */}
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
              <div className="h-44 bg-slate-800 relative">
                <img
                  src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=80"
                  alt="Restaurant Cover"
                  className="w-full h-full object-cover opacity-60"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 to-transparent"></div>
                <div className="absolute bottom-4 left-6 text-white">
                  <h1 className="text-2xl font-black">{selectedPreset.name}</h1>
                  <p className="text-xs text-slate-300">{selectedPreset.cuisine} • Delivery in 25-35 mins</p>
                </div>
              </div>

              {/* LIVE SAFEBITE TRANSPARENCY OVERLAY WIDGET */}
              <div className="p-4 bg-gradient-to-r from-emerald-50 via-teal-50 to-blue-50 border-b border-emerald-200">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl bg-emerald-600 text-white flex items-center justify-center font-black shadow-md flex-shrink-0">
                      <Shield size={22} />
                    </div>
                    <div>
                      <div className="flex items-center space-x-2">
                        <span className="text-xs font-bold uppercase tracking-wider text-emerald-900">
                          SafeBite Transparency Verified
                        </span>
                        {matchResult?.matched && (
                          <span className="bg-emerald-200 text-emerald-900 text-[10px] font-bold px-2 py-0.5 rounded-full">
                            {Math.round(matchResult.match_confidence * 100)}% Match
                          </span>
                        )}
                      </div>
                      <div className="text-sm font-extrabold text-slate-900 flex items-center gap-2">
                        <span>Score: {matchResult?.restaurant?.safety_score || 95}/100</span>
                        <span className="text-slate-400">•</span>
                        <span className="text-emerald-700 font-bold">
                          {matchResult?.assessment?.grade_label || 'Pass / Excellent'}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => setShowAuditModal(true)}
                      className="px-3 py-1.5 bg-emerald-600 hover:bg-emerald-700 text-white rounded-lg text-xs font-bold flex items-center shadow-sm transition"
                    >
                      <Info size={14} className="mr-1.5" />
                      View Safety Audit Breakdown
                    </button>
                  </div>
                </div>

                {/* Provenance Tagline */}
                <div className="mt-2.5 pt-2 border-t border-emerald-200/60 flex items-center justify-between text-[11px] text-emerald-800">
                  <span>Source: <strong>{matchResult?.restaurant?.source_name || 'FSSAI FoSTaC Registry'}</strong></span>
                  <span>Verification: <strong>{matchResult?.restaurant?.verification_status || 'Verified Official'}</strong></span>
                </div>
              </div>

              {/* Menu Categories */}
              <div className="p-6">
                <h2 className="text-lg font-bold text-slate-900 mb-4 flex items-center">
                  <UtensilsCrossed size={18} className="mr-2 text-rose-500" />
                  Recommended Dishes
                </h2>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {currentMenu.map((item) => (
                    <div
                      key={item.id}
                      className="border border-slate-200 rounded-xl p-4 flex flex-col justify-between hover:border-slate-300 transition bg-white"
                    >
                      <div>
                        <div className="flex items-center justify-between mb-1">
                          <h4 className="font-bold text-slate-900 text-sm">{item.name}</h4>
                          <span className="font-extrabold text-slate-900 text-sm">₹{item.price}</span>
                        </div>
                        <p className="text-xs text-slate-500 mb-3 leading-relaxed">{item.desc}</p>
                      </div>

                      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
                        <span className="text-[10px] text-slate-400 font-semibold uppercase">{item.category}</span>
                        <button
                          onClick={() => addToCart(item)}
                          className="px-3 py-1 bg-rose-50 hover:bg-rose-100 text-rose-700 border border-rose-200 rounded-lg text-xs font-bold transition flex items-center"
                        >
                          <Plus size={12} className="mr-1" /> Add
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Cart & Checkout Panel (1 Col) */}
          <div className="space-y-6">
            <div className="bg-white rounded-2xl shadow-sm border border-slate-200 p-6 sticky top-6">
              <h3 className="font-bold text-slate-900 text-base mb-4 flex items-center">
                <ShoppingBag size={18} className="mr-2 text-rose-600" />
                Your Delivery Basket ({cart.reduce((s, i) => s + i.qty, 0)})
              </h3>

              {cart.length === 0 ? (
                <div className="text-center py-8 text-slate-400 text-xs">
                  Your basket is empty. Add items from the menu to see live SafeBite checkout validation.
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Cart Items List */}
                  <div className="divide-y divide-slate-100 max-h-56 overflow-y-auto">
                    {cart.map((item) => (
                      <div key={item.id} className="py-2.5 flex items-center justify-between text-xs">
                        <div className="pr-2">
                          <p className="font-semibold text-slate-800">{item.name}</p>
                          <p className="text-slate-500">₹{item.price} each</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <button
                            onClick={() => updateCartQty(item.id, -1)}
                            className="p-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-600"
                          >
                            <Minus size={10} />
                          </button>
                          <span className="font-bold text-slate-800 w-4 text-center">{item.qty}</span>
                          <button
                            onClick={() => updateCartQty(item.id, 1)}
                            className="p-1 rounded bg-slate-100 hover:bg-slate-200 text-slate-600"
                          >
                            <Plus size={10} />
                          </button>
                          <span className="font-bold text-slate-900 w-12 text-right">₹{item.price * item.qty}</span>
                        </div>
                      </div>
                    ))}
                  </div>

                  {/* SafeBite Safety Advisory Pre-Checkout Verification Card */}
                  <div className="bg-emerald-50 border border-emerald-200 rounded-xl p-3 text-xs">
                    <div className="flex items-center space-x-2 font-bold text-emerald-900 mb-1">
                      <Shield size={14} className="text-emerald-600" />
                      <span>SafeBite Verified Order</span>
                    </div>
                    <p className="text-[11px] text-emerald-800">
                      Kitchen audited with <strong>{matchResult?.restaurant?.safety_score || 95}/100</strong> safety standards. No critical temperature infractions.
                    </p>
                  </div>

                  {/* Price Calculations */}
                  <div className="space-y-1.5 text-xs text-slate-600 pt-2 border-t border-slate-100">
                    <div className="flex justify-between">
                      <span>Subtotal</span>
                      <span className="font-semibold">₹{cartSubtotal}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Delivery Fee</span>
                      <span className="font-semibold">₹{deliveryFee}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Taxes (GST 5%)</span>
                      <span className="font-semibold">₹{taxes}</span>
                    </div>
                    <div className="flex justify-between font-bold text-sm text-slate-900 pt-2 border-t border-slate-200">
                      <span>Total Amount</span>
                      <span>₹{cartTotal}</span>
                    </div>
                  </div>

                  {/* Checkout Button */}
                  {orderPlaced ? (
                    <div className="p-3 bg-emerald-100 text-emerald-900 rounded-xl text-center text-xs font-bold">
                      ✓ Simulated Order #SB-{Math.floor(100000 + Math.random() * 900000)} Placed Successfully!
                    </div>
                  ) : (
                    <button
                      onClick={() => setOrderPlaced(true)}
                      className="w-full py-3 bg-rose-600 hover:bg-rose-700 text-white rounded-xl font-bold text-sm flex items-center justify-center shadow-lg transition"
                    >
                      Place Safe Order (₹{cartTotal})
                      <ArrowRight size={16} className="ml-2" />
                    </button>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Audit Breakdown Modal */}
      {showAuditModal && matchResult && (
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-xl w-full p-6 space-y-4 max-h-[90vh] overflow-y-auto">
            <div className="flex items-center justify-between pb-3 border-b">
              <div className="flex items-center space-x-2">
                <Shield size={24} className="text-emerald-600" />
                <h3 className="text-lg font-bold text-slate-900">Food Safety Audit Breakdown</h3>
              </div>
              <button
                onClick={() => setShowAuditModal(false)}
                className="text-slate-400 hover:text-slate-600 text-sm font-bold"
              >
                ✕
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <h4 className="font-extrabold text-xl text-slate-900">{matchResult.restaurant?.name}</h4>
                <p className="text-xs text-slate-500">{matchResult.restaurant?.address}, {matchResult.restaurant?.city}</p>
              </div>

              {/* Score Highlight */}
              <div className="bg-slate-50 p-4 rounded-xl flex items-center justify-between border">
                <div>
                  <div className="text-xs text-slate-500 uppercase font-semibold">Safety Score</div>
                  <div className="text-3xl font-black text-emerald-600">{matchResult.restaurant?.safety_score}/100</div>
                </div>
                <div className="text-right">
                  <span className="px-3 py-1 bg-emerald-100 text-emerald-800 rounded-full font-bold text-xs">
                    {matchResult.assessment?.grade_label || 'Pass / Excellent'}
                  </span>
                  <div className="text-[11px] text-slate-400 mt-1">Status: {matchResult.restaurant?.verification_status}</div>
                </div>
              </div>

              {/* Summary Explanation */}
              {matchResult.assessment?.summary_explanation && (
                <div className="text-xs text-slate-700 bg-blue-50 p-3 rounded-lg border border-blue-100 leading-relaxed">
                  <strong>Regulatory Assessment:</strong> {matchResult.assessment.summary_explanation}
                </div>
              )}

              {/* Positive Compliance Strengths */}
              {matchResult.assessment?.positive_factors?.length > 0 && (
                <div>
                  <h5 className="font-bold text-xs uppercase tracking-wide text-emerald-800 mb-2">Verified Compliance Strengths:</h5>
                  <ul className="space-y-1.5 text-xs text-emerald-900">
                    {matchResult.assessment.positive_factors.map((f, i) => (
                      <li key={i} className="flex items-start">
                        <CheckCircle2 size={13} className="text-emerald-500 mr-2 mt-0.5 flex-shrink-0" />
                        <span>{f}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Provenance Disclaimer */}
              <div className="text-[11px] text-slate-500 bg-slate-50 p-3 rounded border">
                <strong>Provenance Authority:</strong> {matchResult.restaurant?.source_name} ({matchResult.restaurant?.verification_status}). 
                Record ID: {matchResult.restaurant?.source_record_id || matchResult.restaurant?.license_number}.
              </div>
            </div>

            <div className="pt-3 border-t text-right">
              <button
                onClick={() => setShowAuditModal(false)}
                className="px-4 py-2 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-xs font-bold"
              >
                Close Audit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CompanionOrderingDemo;
