import * as React from "react";
import { Box, Button, Code, Grid, Text, VStack } from "@chakra-ui/react";
import { ColorModeSwitcher } from "../ColorModeSwitcher";
import { Logo } from "../Logo";
import { useNavigate } from "react-router-dom";


const Home: React.FC = () => {
  const navigate = useNavigate();

  const routeTo = (destination: string): void => {
    navigate(destination);
  };

  return (
    <Box textAlign="center" fontSize="xl">
      <Grid minH="100vh" p={3}>
        <ColorModeSwitcher justifySelf="flex-end" />
        <VStack spacing={8}>
          <Logo h="40vmin" pointerEvents="none" />
          <Text>
            This is the Home page.
          </Text>
          <Button colorScheme="teal" onClick={() => routeTo('/about')}>
            About
          </Button>
        </VStack>
      </Grid>
    </Box>
  );
};

export default Home;