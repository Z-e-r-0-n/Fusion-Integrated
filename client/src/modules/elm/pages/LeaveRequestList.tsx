// Leave Request List
import { Table, Thead, Tbody, Tr, Th, Td, Paper, Stack, Title, Button, LoadingOverlay, Text } from '@mantine/core';
import { useLeaveRequests, useApproveLeave } from '../../api/hooks';
import { useNavigate } from 'react-router-dom';

export default function LeaveRequestList() {
  const { data, isLoading, error } = useLeaveRequests();
  const { mutateAsync } = useApproveLeave();
  const navigate = useNavigate();

  if (isLoading) return (
    <Paper p="md">
      <LoadingOverlay visible={true} overlayOpacity={0.1}>
        <Title order={3}>Leave Requests</Title>
        <Text>Loading requests...</Text>
      </LoadingOverlay>
    </Paper>
  );

  if (error) return (
    <Paper p="md">
      <Title order={3}>Leave Requests</Title>
      <Text color="red">{error.message}</Text>
    </Paper>
  );

  return (
    <Paper p="md">
      <Title order={3}>Leave Requests</Title>
      <Table>
        <Thead>
          <Tr>
            <Th>ID</Th>
            <Th>Employee</Th>
            <Th>Start Date</Th>
            <Th>Status</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data.map((request) => (
            <Tr key={request.id}>
              <Td>{request.id}</Td>
              <Td>{request.employee.name}</Td>
              <Td>{request.start_date}</Td>
              <Td>
                <StatusBadge color={request.status === 'APPROVED' ? 'green' : 'yellow'}>
                  {request.status}
                </StatusBadge>
              </Td>
              <Td>
                <Stack>
                  <Button
                    variant="default"
                    onClick={() => navigate(`/elm/requests/${request.id}`)}
                  >
                    View
                  </Button>
                  {request.status === 'PENDING' && (
                    <Button
                      color="blue"
                      onClick={() => mutateAsync({ request_id: request.id, status: 'APPROVED' })}
                    >
                      Approve
                    </Button>
                  )}
                  {request.status === 'PENDING' && (
                    <Button
                      color="red"
                      onClick={() => mutateAsync({ request_id: request.id, status: 'REJECTED' })}
                    >
                      Reject
                    </Button>
                  )}
                </Stack>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Paper>
  );
}