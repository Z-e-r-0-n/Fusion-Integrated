// ELM API hooks
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { http } from '../../../lib/http';
import type { AxiosError } from 'axios';

// Leave Requests
export const useLeaveRequests = () => {
  return useQuery({
    queryKey: ['leave-requests'],
    queryFn: async () => {
      const { data } = await http.get('/api/v1/elm/requests');
      return data;
    }
  });
};

export const useApproveLeave = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async ({ request_id, status }: { request_id: number; status: 'APPROVED' | 'REJECTED' }) => {
      await http.patch(`/api/v1/elm/requests/${request_id}/status`, { status });
      await queryClient.invalidateQueries(['leave-requests']);
    }
  });
};

// Leave Balances
export const useLeaveBalances = () => {
  return useQuery({
    queryKey: ['leave-balances'],
    queryFn: async () => {
      const { data } = await http.get('/api/v1/elm/balances');
      return data;
    }
  });
};

// Leave Types
export const useLeaveTypes = () => {
  return useQuery({
    queryKey: ['leave-types'],
    queryFn: async () => {
      const { data } = await http.get('/api/v1/elm/types');
      return data;
    }
  });
};

// Leave Policies
export const useLeavePolicies = () => {
  return useQuery({
    queryKey: ['leave-policies'],
    queryFn: async () => {
      const { data } = await http.get('/api/v1/elm/policies');
      return data;
    }
  });
};