// Leave Policy Editor
import { Table, Thead, Tbody, Tr, Th, Td, Paper, Stack, Title, Button, LoadingOverlay, Text, Select } from '@mantine/core';
import { useLeavePolicies } from '../../api/hooks';
import { useNavigate } from 'react-router-dom';

export default function LeavePolicyEditor() {
  const { data, isLoading, error } = useLeavePolicies();
  const navigate = useNavigate();

  if (isLoading) return (
    <Paper p="md">
      <LoadingOverlay visible={true} overlayOpacity={0.1}>
        <Title order={3}>Leave Policies</Title>
        <Text>Loading policies...</Text>
      </LoadingOverlay>
    </Paper>
  );

  if (error) return (
    <Paper p="md">
      <Title order={3}>Leave Policies</Title>
      <Text color="red">{error.message}</Text>
    </Paper>
  );

  return (
    <Paper p="md">
      <Title order={3}>Leave Policies</Title>
      <Table>
        <Thead>
          <Tr>
            <Th>Name</Th>
            <Th>Description</Th>
            <Th>Status</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {data.map((policy) => (
            <Tr key={policy.id}>
              <Td>{policy.name}</Td>
              <Td>{policy.description}</Td>
              <Td>
                <StatusBadge color={policy.status === 'ACTIVE' ? 'green' : 'yellow'}>
                  {policy.status}
                </StatusBade>
              </Td>
              <Td>
                <Stack>
                  <Button
                    variant="default"
                    onClick={() => navigate(`/elm/policies/${policy.id}`)}
                  >
                    View
                  </Button>
                  <Button
                    color="blue"
                    onClick={() => navigate(`/elm/policies/${policy.id}/edit`)}
                  >
                    Edit
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