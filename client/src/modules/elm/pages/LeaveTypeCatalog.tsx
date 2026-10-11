// Leave Type Catalog
import { Table, Thead, Tbody, Tr, Th, Td, Paper, Stack, Title, Button, LoadingOverlay, Text } from '@mantine/core';
import { useLeaveTypes } from '../../api/hooks';
import { useNavigate } from 'react-router-dom';

export default function LeaveTypeCatalog() {
  const { data, isLoading, error } = useLeaveTypes();
  const navigate = useNavigate();

  if (isLoading) return (
    <Paper p="md">
      <LoadingOverlay visible={true} overlayOpacity={0.1}>
        <Title order={3}>Leave Types</Title>
        <Text>Loading types...</Text>
      </LoadingOverlay>
    </Paper>
  );

  if (error) return (
    <Paper p="md">
      <Title order={3}>Leave Types</Title>
      <Text color="red">{error.message}</Text>
    </Paper>
  );

  return (
    <Paper p="md">
      <Title order={3}>Leave Types</Title>
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
          {data.map((type) => (
            <Tr key={type.id}>
              <Td>{type.name}</Td>
              <Td>{type.description}</Td>
              <Td>
                <StatusBadge color={type.status === 'ACTIVE' ? 'green' : 'yellow'}>
                  {type.status}
                </StatusBadge>
              </Td>
              <Td>
                <Stack>
                  <Button
                    variant="default"
                    onClick={() => navigate(`/elm/types/${type.id}`)}
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