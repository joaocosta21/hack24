import * as React from "react";
import { Box, Button, Code, Grid, Text, VStack } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const About: React.FC = () => {
  const navigate = useNavigate();

  const routeTo = (destination: string): void => {
    navigate(destination);
  };

  return (
    <Box textAlign="center" fontSize="xl">
      <Grid minH="100vh" p={3}>
        <VStack spacing={8}>
          <Text>
            This is the About page.
          </Text>
          <Button colorScheme="teal" onClick={() => routeTo('/')}>
            About
          </Button>
        </VStack>
      </Grid>
    </Box>
  );
};

export default About;