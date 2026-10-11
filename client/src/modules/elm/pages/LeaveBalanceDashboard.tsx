// Leave Balance Dashboard
import { Table, Thead, Tbody, Tr, Th, Td, Paper, Stack, Title, Button, LoadingOverlay, Text } from '@mantine/core';
import { useLeaveBalances } from '../../api/hooks';
import { useNavigate } from 'react-router-dom';

export default function LeaveBalanceDashboard() {
  const { data, isLoading, error } = useLeaveBalances();
  const navigate = useNavigate();

  if (isLoading) return (
    <Paper p="md">
      <LoadingOverlay visible={true} overlayOpacity={0.1}>
        <Title order={3}>Leave Balance</Title>
        <Text>Loading balances...</Text>
      </LoadingOverlay>
    </Paper>
  );

  if (error) return (
    <Paper p="md">
      <Title order={3}>Leave Balance</Title>
      <Text color="red">{error.message}</Text>
    </Paper>
  );

  return (
    <Paper p="md">
      <Title order={3}>Leave Balance</Title>
      <Table>
        <Thead>
          <Tr>
            <Th>Employee</Th>
            <Th>Annual Balance</Th>
            <Th>Used</Th>
            <Th>Remaining</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data.map((balance) => (
            <Tr key={balance.id}>
              <Td>{balance.employee.name}</Td>
              <Td>{balance.annual_balance}</Td>
              <Td>{balance.used}</Td>
              <Td>{balance.remaining}</Td>
              <Td>
                <Stack>
                  <Button
                    variant="default"
                    onClick={() => navigate(`/elm/balances/${balance.id}`)}
                  >
                    View
                  </Button>
                </Stack>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Paper>
  );
}