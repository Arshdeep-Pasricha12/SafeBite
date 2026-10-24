import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { 
  MapPin, Phone, Mail, Clock, Star, Shield, AlertTriangle, 
  CheckCircle, Camera, ExternalLink, FileText, Send, Info, CheckCircle2 
} from 'lucide-react';
import { restaurantApi } from '../services/api';
import { useAuth } from '../context/AuthContext';
import InspectionHistory from '../components/InspectionHistory';

const RestaurantDetail = () => {
  const { id } = useParams();
  const { user } = useAuth();
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState('assessment'); // Default to assessment tab

  // Correction Request State
  const [showCorrectionModal, setShowCorrectionModal] = useState(false);
  const [correctionType, setCorrectionType] = useState('Data Correction');
  const [correctionDetails, setCorrectionDetails] = useState('');
  const [evidenceUrl, setEvidenceUrl] = useState('');
  const [submittingCorrection, setSubmittingCorrection] = useState(false);
  const [correctionSuccess, setCorrectionSuccess] = useState(false);
  const [correctionRequests, setCorrectionRequests] = useState([]);

  useEffect(() => {
    fetchRestaurant();
    fetchCorrectionRequests();
  }, [id]);

  const fetchRestaurant = async () => {
    try {
      setLoading(true);
      const response = await restaurantApi.getById(id);
      setRestaurant(response.data);
    } catch (err) {
      console.error('Error fetching restaurant:', err);
      setError('Restaurant not found');
    } finally {
      setLoading(false);
    }
  };

  const fetchCorrectionRequests = async () => {
    try {
      if (user && (user.role === 'owner' || user.role === 'admin')) {
        const response = await restaurantApi.getCorrectionRequests(id);
        setCorrectionRequests(response.data);
      }
    } catch (err) {
      console.log('Correction requests load skipped (auth restricted)');
    }
  };

  const handleCorrectionSubmit = async (e) => {
    e.preventDefault();
    if (!correctionDetails.trim()) return;

    try {
      setSubmittingCorrection(true);
      await restaurantApi.submitCorrectionRequest(id, {
        restaurant_id: id,
        request_type: correctionType,
        details: correctionDetails,
        evidence_url: evidenceUrl || null
      });
      setCorrectionSuccess(true);
      setCorrectionDetails('');
      setEvidenceUrl('');
      fetchCorrectionRequests();
      setTimeout(() => {
        setShowCorrectionModal(false);
        setCorrectionSuccess(false);
      }, 2000);
    } catch (err) {
      alert(err.response?.data?.detail || 'Failed to submit correction request.');
    } finally {
      setSubmittingCorrection(false);
    }
  };

  const getSafetyBadgeColor = (rating) => {
    switch (rating?.toLowerCase()) {
      case 'excellent':
        return 'bg-green-100 text-green-800 border-green-200';
      case 'good':
        return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'fair':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      case 'poor':
        return 'bg-red-100 text-red-800 border-red-200';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600';
    if (score >= 80) return 'text-blue-600';
    if (score >= 70) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="animate-pulse">
            <div className="h-64 bg-gray-200 rounded-lg mb-6"></div>
            <div className="h-8 bg-gray-200 rounded mb-4"></div>
            <div className="h-4 bg-gray-200 rounded mb-2"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    );
  }

  if (error || !restaurant) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <AlertTriangle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h1 className="text-2xl font-bold text-gray-900 mb-2">Restaurant Not Found</h1>
          <p className="text-gray-600">{error || 'Unable to load restaurant details.'}</p>
        </div>
      </div>
    );
  }

  const assessment = restaurant.assessment;

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Provenance Transparency Header Banner */}
      {!restaurant.is_synthetic ? (
        <div className="bg-emerald-900 text-emerald-100 px-4 py-3 shadow-inner">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between text-sm gap-2">
            <div className="flex items-center space-x-2">
              <Shield className="w-5 h-5 text-emerald-400 flex-shrink-0" />
              <span className="font-bold text-white tracking-wide">VERIFIED OFFICIAL RECORD:</span>
              <span>Sourced from {restaurant.source_name || 'Public Health Authority'}.</span>
            </div>
            <div className="flex items-center space-x-4 text-xs text-emerald-200">
              <span>Status: <strong className="text-white">{restaurant.verification_status}</strong></span>
              <span>Freshness: <strong className="text-white">{restaurant.data_freshness_status}</strong></span>
              {restaurant.source_url && (
                <a 
                  href={restaurant.source_url} 
                  target="_blank" 
                  rel="noopener noreferrer" 
                  className="inline-flex items-center text-emerald-300 hover:text-white underline font-semibold"
                >
                  Verify Source <ExternalLink size={12} className="ml-1" />
                </a>
              )}
            </div>
          </div>
        </div>
      ) : (
        <div className="bg-amber-900 text-amber-100 px-4 py-3 shadow-inner">
          <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-start md:items-center justify-between text-sm gap-2">
            <div className="flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 text-amber-400 flex-shrink-0" />
              <span className="font-bold text-white tracking-wide">DEMONSTRATION BENCHMARK:</span>
              <span>This record is generated from synthetic simulated benchmark data for testing and demonstration.</span>
            </div>
            <div className="text-xs text-amber-200">
              Confidence: {Math.round((restaurant.confidence_score || 0.75) * 100)}% | Not a live regulatory filing
            </div>
          </div>
        </div>
      )}

      {/* Hero Section */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-6xl mx-auto p-8">
          <div className="grid md:grid-cols-3 gap-8">
            {/* Restaurant Image */}
            <div className="md:col-span-1">
              {restaurant.images && restaurant.images.length > 0 ? (
                <img
                  src={restaurant.images[0].image_url}
                  alt={restaurant.name}
                  className="w-full h-64 object-cover rounded-lg shadow-lg"
                />
              ) : (
                <div className="w-full h-64 bg-gray-200 rounded-lg flex items-center justify-center">
                  <Camera className="w-12 h-12 text-gray-400" />
                </div>
              )}
            </div>

            {/* Restaurant Info */}
            <div className="md:col-span-2">
              <div className="flex flex-col sm:flex-row items-start justify-between gap-4 mb-4">
                <div>
                  <h1 className="text-4xl font-bold text-gray-900 mb-2">{restaurant.name}</h1>
                  <p className="text-lg text-gray-600 mb-4">{restaurant.cuisine} Cuisine</p>
                  
                  <div className="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-4">
                    <span className="flex items-center">
                      <MapPin className="w-4 h-4 mr-1 text-gray-400" />
                      {restaurant.address}, {restaurant.city}, {restaurant.state}
                    </span>
                    <span className="flex items-center">
                      <Phone className="w-4 h-4 mr-1 text-gray-400" />
                      {restaurant.phone}
                    </span>
                  </div>

                  <div className="text-xs text-gray-500 font-mono">
                    License #{restaurant.license_number} ({restaurant.license_status})
                  </div>
                </div>

                {/* Safety Score Card */}
                <div className="text-center bg-white border-2 border-gray-200 rounded-xl p-5 shadow-lg min-w-[160px]">
                  <div className="mb-1">
                    <Shield className="w-7 h-7 mx-auto text-blue-600 mb-1" />
                    <div className="text-xs text-gray-500 uppercase tracking-wide font-semibold">
                      Safety Score
                    </div>
                  </div>
                  <div className={`text-4xl font-extrabold ${getScoreColor(restaurant.safety_score)} mb-1`}>
                    {restaurant.safety_score}
                  </div>
                  <div className={`px-3 py-0.5 rounded-full text-xs font-bold border ${getSafetyBadgeColor(restaurant.safety_rating)}`}>
                    {assessment?.grade_label || restaurant.safety_rating}
                  </div>
                  {restaurant.data_freshness_status === 'Stale' && (
                    <div className="mt-1 text-[11px] font-bold text-amber-600 bg-amber-50 rounded px-1.5 py-0.5">
                      ⚠️ Stale Data Warning
                    </div>
                  )}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="flex items-center gap-3 mt-4 pt-4 border-t border-gray-100">
                <button
                  onClick={() => setShowCorrectionModal(true)}
                  className="inline-flex items-center text-xs font-semibold px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-lg transition"
                >
                  <FileText size={14} className="mr-1.5" />
                  Submit Data Correction / Dispute
                </button>
                {restaurant.source_url && (
                  <a
                    href={restaurant.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-xs font-semibold px-3 py-2 bg-blue-50 hover:bg-blue-100 text-blue-700 rounded-lg transition"
                  >
                    <ExternalLink size={14} className="mr-1.5" />
                    Audit Registry Source
                  </a>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-6xl mx-auto">
          <nav className="flex space-x-8 px-8 overflow-x-auto">
            <button
              onClick={() => setActiveTab('assessment')}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === 'assessment'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Shield size={16} className="mr-2" />
              Safety Assessment & Explainability
            </button>
            <button
              onClick={() => setActiveTab('inspections')}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === 'inspections'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Clock size={16} className="mr-2" />
              Inspection History
            </button>
            <button
              onClick={() => setActiveTab('details')}
              className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                activeTab === 'details'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              }`}
            >
              <Info size={16} className="mr-2" />
              Provenance & Details
            </button>
            {correctionRequests.length > 0 && (
              <button
                onClick={() => setActiveTab('corrections')}
                className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center ${
                  activeTab === 'corrections'
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <FileText size={16} className="mr-2" />
                Disputes & Corrections ({correctionRequests.length})
              </button>
            )}
          </nav>
        </div>
      </div>

      {/* Tab Content */}
      <div className="max-w-6xl mx-auto p-8">
        {/* Explainable Safety Assessment Tab */}
        {activeTab === 'assessment' && (
          <div className="space-y-6">
            {assessment ? (
              <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-6">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <h2 className="text-2xl font-bold text-gray-900 flex items-center">
                      <Shield className="w-6 h-6 text-blue-600 mr-2" />
                      Explainable Food Safety Risk Evaluation
                    </h2>
                    <span className="text-xs bg-blue-50 text-blue-700 font-bold px-3 py-1 rounded-full border border-blue-200">
                      Deterministic Policy Engine v1.0
                    </span>
                  </div>
                  <p className="text-gray-700 font-medium text-lg bg-gray-50 p-4 rounded-lg border border-gray-100">
                    {assessment.summary_explanation}
                  </p>
                </div>

                {/* Consumer Guidance Alert */}
                <div className={`p-4 rounded-lg border flex items-start space-x-3 ${
                  assessment.safety_score >= 80 
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-900' 
                    : assessment.safety_score >= 60 
                    ? 'bg-amber-50 border-amber-200 text-amber-900'
                    : 'bg-red-50 border-red-200 text-red-900'
                }`}>
                  <CheckCircle2 className="w-5 h-5 mt-0.5 flex-shrink-0" />
                  <div>
                    <h4 className="font-bold text-sm uppercase tracking-wide">Consumer Dining Guidance</h4>
                    <p className="text-sm mt-0.5">{assessment.consumer_advice}</p>
                  </div>
                </div>

                {/* Risk and Positive Factors Split Grid */}
                <div className="grid md:grid-cols-2 gap-6">
                  {/* Positive Compliance Factors */}
                  <div className="border border-emerald-200 bg-emerald-50/50 rounded-xl p-5">
                    <h3 className="font-bold text-emerald-900 flex items-center mb-3">
                      <CheckCircle className="w-5 h-5 text-emerald-600 mr-2" />
                      Compliance Strengths ({assessment.positive_factors.length})
                    </h3>
                    {assessment.positive_factors.length > 0 ? (
                      <ul className="space-y-2 text-sm text-emerald-800">
                        {assessment.positive_factors.map((factor, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-emerald-500 font-bold mr-2">✓</span>
                            <span>{factor}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-sm text-gray-500">No positive factors recorded.</p>
                    )}
                  </div>

                  {/* Risk Factors & Point Deductions */}
                  <div className="border border-rose-200 bg-rose-50/50 rounded-xl p-5">
                    <h3 className="font-bold text-rose-900 flex items-center mb-3">
                      <AlertTriangle className="w-5 h-5 text-rose-600 mr-2" />
                      Risk Citations & Deductions ({assessment.risk_factors.length})
                    </h3>
                    {assessment.risk_factors.length > 0 ? (
                      <ul className="space-y-2 text-sm text-rose-800">
                        {assessment.risk_factors.map((factor, idx) => (
                          <li key={idx} className="flex items-start">
                            <span className="text-rose-500 font-bold mr-2">⚠️</span>
                            <span>{factor}</span>
                          </li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-sm text-emerald-700 font-medium">
                        ✓ Zero risk infractions or score deductions on current cycle.
                      </p>
                    )}
                  </div>
                </div>

                {/* Audit Provenance Disclaimer */}
                <div className="p-4 bg-gray-50 border border-gray-200 rounded-lg text-xs text-gray-600">
                  <div className="font-bold text-gray-700 uppercase mb-1">Audit Provenance Disclaimer:</div>
                  <p>{assessment.provenance_disclaimer}</p>
                </div>
              </div>
            ) : (
              <div className="bg-white p-6 rounded-lg shadow text-center text-gray-500">
                Evaluation data generating...
              </div>
            )}
          </div>
        )}

        {/* Inspections Tab */}
        {activeTab === 'inspections' && (
          <div className="space-y-8">
            <InspectionHistory restaurantId={restaurant.id} />
          </div>
        )}

        {/* Provenance & Details Tab */}
        {activeTab === 'details' && (
          <div className="bg-white rounded-lg shadow p-6 space-y-6">
            <h2 className="text-2xl font-bold text-gray-900">Regulatory Details & Provenance</h2>
            
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-3 text-sm">
                <h3 className="font-bold text-gray-800 text-base">Entity Identification</h3>
                <div><span className="text-gray-500">Restaurant ID:</span> <span className="font-mono font-semibold">{restaurant.id}</span></div>
                <div><span className="text-gray-500">License Number:</span> <span className="font-mono font-semibold">{restaurant.license_number}</span></div>
                <div><span className="text-gray-500">License Status:</span> <span className="font-semibold">{restaurant.license_status}</span></div>
                <div><span className="text-gray-500">Operating Hours:</span> <span>{restaurant.opening_hours}</span></div>
                <div><span className="text-gray-500">Contact Email:</span> <span>{restaurant.email}</span></div>
                <div><span className="text-gray-500">Phone:</span> <span>{restaurant.phone}</span></div>
              </div>

              <div className="space-y-3 text-sm">
                <h3 className="font-bold text-gray-800 text-base">Traceability Metadata</h3>
                <div><span className="text-gray-500">Source Authority:</span> <span className="font-semibold">{restaurant.source_name || 'Benchmark Dataset'}</span></div>
                <div><span className="text-gray-500">Verification Status:</span> <span className="font-semibold">{restaurant.verification_status}</span></div>
                <div><span className="text-gray-500">Data Freshness:</span> <span className="font-semibold">{restaurant.data_freshness_status}</span></div>
                <div><span className="text-gray-500">Synthetic Benchmark:</span> <span>{restaurant.is_synthetic ? 'Yes (Simulated)' : 'No (Genuine Public Data)'}</span></div>
                <div><span className="text-gray-500">Source Record ID:</span> <span className="font-mono">{restaurant.source_record_id || 'N/A'}</span></div>
                {restaurant.source_url && (
                  <div>
                    <span className="text-gray-500">Public URL:</span>{' '}
                    <a href={restaurant.source_url} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline">
                      {restaurant.source_url}
                    </a>
                  </div>
                )}
              </div>
            </div>

            {restaurant.description && (
              <div className="pt-4 border-t border-gray-100">
                <h3 className="font-bold text-gray-800 mb-2">Description</h3>
                <p className="text-gray-700 text-sm leading-relaxed">{restaurant.description}</p>
              </div>
            )}
          </div>
        )}

        {/* Disputes & Corrections Tab */}
        {activeTab === 'corrections' && (
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900">Submitted Disputes & Correction Requests</h2>
              <button
                onClick={() => setShowCorrectionModal(true)}
                className="text-xs bg-blue-600 text-white px-3 py-1.5 rounded-lg hover:bg-blue-700 font-semibold"
              >
                + Submit New Request
              </button>
            </div>

            <div className="divide-y divide-gray-100">
              {correctionRequests.map(req => (
                <div key={req.id} className="py-4">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-bold text-gray-900 text-sm">{req.request_type}</span>
                    <span className={`px-2 py-0.5 rounded text-xs font-semibold ${
                      req.status === 'Approved' ? 'bg-emerald-100 text-emerald-800' :
                      req.status === 'Rejected' ? 'bg-rose-100 text-rose-800' :
                      'bg-amber-100 text-amber-800'
                    }`}>
                      {req.status}
                    </span>
                  </div>
                  <p className="text-gray-700 text-sm mb-2">{req.details}</p>
                  {req.admin_notes && (
                    <div className="text-xs bg-gray-50 p-2 rounded border border-gray-200 text-gray-600">
                      <strong>Admin Response:</strong> {req.admin_notes}
                    </div>
                  )}
                  <div className="text-[11px] text-gray-400 mt-1">
                    Submitted: {new Date(req.created_at).toLocaleString()}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Correction Request Modal */}
      {showCorrectionModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-xl shadow-2xl max-w-lg w-full p-6 space-y-4">
            <h3 className="text-xl font-bold text-gray-900">Submit Data Correction or Dispute</h3>
            <p className="text-xs text-gray-500">
              As a restaurant owner or designated representative, you may submit correction requests for inaccurate inspection records or updated certifications.
            </p>

            {correctionSuccess ? (
              <div className="p-4 bg-emerald-50 text-emerald-800 rounded-lg text-sm text-center font-bold">
                ✓ Request submitted successfully for administrative review.
              </div>
            ) : (
              <form onSubmit={handleCorrectionSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-bold text-gray-700 mb-1">Request Type</label>
                  <select
                    value={correctionType}
                    onChange={(e) => setCorrectionType(e.target.value)}
                    className="w-full text-sm border rounded-lg p-2.5"
                  >
                    <option value="Data Correction">Data Correction (Hours, Address, Details)</option>
                    <option value="Inspection Dispute">Inspection Dispute (Contest Citation)</option>
                    <option value="License Update">License Update (Renewed Certification)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-700 mb-1">Explanation / Description</label>
                  <textarea
                    rows={4}
                    value={correctionDetails}
                    onChange={(e) => setCorrectionDetails(e.target.value)}
                    placeholder="Provide detailed justification and specifics of the requested update..."
                    className="w-full text-sm border rounded-lg p-2.5"
                    required
                  />
                </div>

                <div>
                  <label className="block text-xs font-bold text-gray-700 mb-1">Supporting Evidence URL (Optional)</label>
                  <input
                    type="url"
                    value={evidenceUrl}
                    onChange={(e) => setEvidenceUrl(e.target.value)}
                    placeholder="https://drive.google.com/... or public document link"
                    className="w-full text-sm border rounded-lg p-2.5"
                  />
                </div>

                <div className="flex justify-end space-x-3 pt-3 border-t">
                  <button
                    type="button"
                    onClick={() => setShowCorrectionModal(false)}
                    className="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg font-medium"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submittingCorrection}
                    className="px-5 py-2 text-sm bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-bold flex items-center"
                  >
                    {submittingCorrection ? 'Submitting...' : 'Submit for Review'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default RestaurantDetail;