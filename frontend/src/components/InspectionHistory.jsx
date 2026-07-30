import React, { useState, useEffect } from 'react';
import { Calendar, User, AlertTriangle, CheckCircle, XCircle, Clock, Camera, MapPin } from 'lucide-react';
import { restaurantApi } from '../services/api';

const InspectionHistory = ({ restaurantId }) => {
  const [inspections, setInspections] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedInspection, setSelectedInspection] = useState(null);

  useEffect(() => {
    fetchInspections();
  }, [restaurantId]);

  const fetchInspections = async () => {
    try {
      setLoading(true);
      const response = await restaurantApi.getInspections(restaurantId);
      setInspections(response.data);
    } catch (err) {
      console.error('Error fetching inspections:', err);
      setError('Failed to load inspection history');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 90) return 'text-green-600 bg-green-100';
    if (score >= 80) return 'text-blue-600 bg-blue-100';
    if (score >= 70) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getRiskColor = (risk) => {
    switch (risk?.toLowerCase()) {
      case 'low': return 'text-green-600 bg-green-100';
      case 'medium': return 'text-yellow-600 bg-yellow-100';
      case 'high': return 'text-red-600 bg-red-100';
      case 'critical': return 'text-red-800 bg-red-200';
      default: return 'text-gray-600 bg-gray-100';
    }
  };

  const getStatusIcon = (status) => {
    switch (status?.toLowerCase()) {
      case 'passed':
        return <CheckCircle className="w-5 h-5 text-green-600" />;
      case 'failed':
        return <XCircle className="w-5 h-5 text-red-600" />;
      default:
        return <AlertTriangle className="w-5 h-5 text-yellow-600" />;
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case 'critical': return 'bg-red-100 text-red-800 border-red-200';
      case 'major': return 'bg-orange-100 text-orange-800 border-orange-200';
      case 'minor': return 'bg-yellow-100 text-yellow-800 border-yellow-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  if (loading) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4"></div>
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="text-center text-red-600">
          <AlertTriangle className="w-12 h-12 mx-auto mb-4" />
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-lg">
      {/* Header */}
      <div className="px-6 py-4 border-b border-gray-200">
        <h2 className="text-2xl font-bold text-gray-900 flex items-center">
          <Calendar className="w-6 h-6 mr-2 text-blue-600" />
          Inspection History
        </h2>
        <p className="text-gray-600 mt-1">
          {inspections.length} inspection{inspections.length !== 1 ? 's' : ''} recorded
        </p>
      </div>

      {/* Inspection Timeline */}
      <div className="p-6">
        {inspections.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            <Calendar className="w-12 h-12 mx-auto mb-4 opacity-50" />
            <p>No inspection history available</p>
          </div>
        ) : (
          <div className="space-y-6">
            {inspections.map((inspection, index) => (
              <div
                key={inspection.id}
                className="relative border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => setSelectedInspection(selectedInspection?.id === inspection.id ? null : inspection)}
              >
                {/* Timeline connector */}
                {index < inspections.length - 1 && (
                  <div className="absolute left-6 top-16 w-0.5 h-6 bg-gray-300"></div>
                )}

                {/* Inspection Summary */}
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-4">
                    <div className="flex-shrink-0">
                      {getStatusIcon(inspection.pass_fail_status)}
                    </div>
                    
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="text-lg font-semibold text-gray-900">
                          {new Date(inspection.inspection_date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric'
                          })}
                        </span>
                        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getRiskColor(inspection.risk_level)}`}>
                          {inspection.risk_level} Risk
                        </span>
                      </div>
                      
                      <div className="flex items-center space-x-4 text-sm text-gray-600 mb-2">
                        <span className="flex items-center">
                          <User className="w-4 h-4 mr-1" />
                          {inspection.inspector?.name || 'Unknown Inspector'}
                        </span>
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {inspection.duration_minutes} minutes
                        </span>
                        <span>{inspection.inspection_type}</span>
                      </div>

                      <div className="flex items-center space-x-4">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${getScoreColor(inspection.total_score)}`}>
                          Score: {inspection.total_score}/100
                        </span>
                        <span className={`px-2 py-1 rounded text-xs ${
                          inspection.pass_fail_status?.toLowerCase() === 'passed' ? 'bg-green-100 text-green-800' :
                          inspection.pass_fail_status?.toLowerCase() === 'failed' ? 'bg-red-100 text-red-800' :
                          'bg-yellow-100 text-yellow-800'
                        }`}>
                          {inspection.pass_fail_status}
                        </span>
                      </div>
                    </div>
                  </div>

                  {/* Violation Summary */}
                  <div className="text-right">
                    <div className="text-2xl font-bold text-gray-900 mb-1">
                      {inspection.violation_count}
                    </div>
                    <div className="text-xs text-gray-500">
                      {inspection.violation_count === 1 ? 'violation' : 'violations'}
                    </div>
                    {inspection.violation_count > 0 && (
                      <div className="flex space-x-1 mt-2">
                        {inspection.critical_violations > 0 && (
                          <span className="px-1 py-0.5 bg-red-100 text-red-800 text-xs rounded">
                            {inspection.critical_violations}C
                          </span>
                        )}
                        {inspection.major_violations > 0 && (
                          <span className="px-1 py-0.5 bg-orange-100 text-orange-800 text-xs rounded">
                            {inspection.major_violations}M
                          </span>
                        )}
                        {inspection.minor_violations > 0 && (
                          <span className="px-1 py-0.5 bg-yellow-100 text-yellow-800 text-xs rounded">
                            {inspection.minor_violations}m
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* Expanded Details */}
                {selectedInspection?.id === inspection.id && (
                  <div className="mt-6 pt-6 border-t border-gray-200">
                    {/* Inspector Details */}
                    {inspection.inspector && (
                      <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                        <h4 className="font-semibold text-blue-900 mb-2">Inspector Information</h4>
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <span className="text-gray-600">Name:</span>
                            <span className="ml-2 font-medium">{inspection.inspector.name}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Badge:</span>
                            <span className="ml-2 font-medium">{inspection.inspector.badge_number}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Level:</span>
                            <span className="ml-2 font-medium">{inspection.inspector.certification_level}</span>
                          </div>
                          <div>
                            <span className="text-gray-600">Department:</span>
                            <span className="ml-2 font-medium">{inspection.inspector.department}</span>
                          </div>
                        </div>
                      </div>
                    )}

                    {/* Violations */}
                    {inspection.violations && inspection.violations.length > 0 && (
                      <div className="mb-6">
                        <h4 className="font-semibold text-gray-900 mb-3">Violations Found</h4>
                        <div className="space-y-3">
                          {inspection.violations.map((violation) => (
                            <div
                              key={violation.id}
                              className={`p-4 rounded-lg border ${getSeverityColor(violation.severity)}`}
                            >
                              <div className="flex items-start justify-between mb-2">
                                <div className="flex items-center space-x-2">
                                  <span className="font-medium text-sm">
                                    Code: {violation.code}
                                  </span>
                                  <span className={`px-2 py-1 rounded text-xs font-medium ${getSeverityColor(violation.severity)}`}>
                                    {violation.severity}
                                  </span>
                                  {violation.repeat_violation && (
                                    <span className="px-2 py-1 bg-red-200 text-red-800 text-xs rounded">
                                      REPEAT
                                    </span>
                                  )}
                                </div>
                                <span className="text-sm font-medium">
                                  -{violation.points_deducted} pts
                                </span>
                              </div>
                              
                              <p className="text-sm text-gray-700 mb-2">
                                {violation.description}
                              </p>
                              
                              <div className="flex items-center justify-between text-xs text-gray-600">
                                <div className="flex items-center space-x-4">
                                  <span className="flex items-center">
                                    <MapPin className="w-3 h-3 mr-1" />
                                    {violation.location}
                                  </span>
                                  <span>Category: {violation.category}</span>
                                </div>
                                <div className="flex items-center space-x-2">
                                  {violation.corrected_on_site ? (
                                    <span className="text-green-600 flex items-center">
                                      <CheckCircle className="w-3 h-3 mr-1" />
                                      Corrected on-site
                                    </span>
                                  ) : (
                                    <span className="text-orange-600 flex items-center">
                                      <Clock className="w-3 h-3 mr-1" />
                                      Requires correction
                                    </span>
                                  )}
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Photos */}
                    {inspection.photos && inspection.photos.length > 0 && (
                      <div className="mb-6">
                        <h4 className="font-semibold text-gray-900 mb-3 flex items-center">
                          <Camera className="w-4 h-4 mr-2" />
                          Inspection Photos ({inspection.photos.length})
                        </h4>
                        <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                          {inspection.photos.map((photo) => (
                            <div key={photo.id} className="bg-gray-100 rounded-lg overflow-hidden">
                              <img
                                src={photo.photo_url}
                                alt={photo.caption}
                                className="w-full h-32 object-cover"
                              />
                              <div className="p-2">
                                <p className="text-xs text-gray-600">{photo.caption}</p>
                                <p className="text-xs text-gray-500">By: {photo.taken_by}</p>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Inspector Notes */}
                    {inspection.inspector_notes && (
                      <div className="p-4 bg-gray-50 rounded-lg">
                        <h4 className="font-semibold text-gray-900 mb-2">Inspector Notes</h4>
                        <p className="text-sm text-gray-700">{inspection.inspector_notes}</p>
                      </div>
                    )}

                    {/* Corrective Actions */}
                    {inspection.corrective_actions_required && (
                      <div className="mt-4 p-4 bg-yellow-50 rounded-lg">
                        <h4 className="font-semibold text-yellow-900 mb-2">Required Corrective Actions</h4>
                        <p className="text-sm text-yellow-800">{inspection.corrective_actions_required}</p>
                      </div>
                    )}

                    {/* Reinspection Info */}
                    {inspection.reinspection_required && (
                      <div className="mt-4 p-4 bg-orange-50 rounded-lg">
                        <h4 className="font-semibold text-orange-900 mb-2">Reinspection Required</h4>
                        {inspection.reinspection_deadline && (
                          <p className="text-sm text-orange-800">
                            Deadline: {new Date(inspection.reinspection_deadline).toLocaleDateString()}
                          </p>
                        )}
                      </div>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default InspectionHistory;