import 'package:flutter/material.dart';
import 'screens/splash_screen.dart';
import 'screens/login_screen.dart';
import 'screens/dados_plantacao_screen.dart';
import 'screens/cadastro_plantacao_screen.dart';
import 'screens/chat_screen.dart';
import 'screens/dashboard_screen.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      initialRoute: '/', // Define a rota inicial como a Splash Screen
      routes: {
        '/': (context) => const SplashScreen(),
        '/login': (context) => const LoginScreen(),
        '/dados': (context) => const DadosPlantacaoScreen(),
        '/cadastro': (context) => const CadastroPlantacaoScreen(),
        '/home': (context) => const DadosPlantacaoScreen(),
        '/chat': (context) => const ChatScreen(),
        '/dashboard': (context) => const DashboardScreen(),
      },
    );
  }
}