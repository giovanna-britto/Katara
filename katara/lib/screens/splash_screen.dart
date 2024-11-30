import 'package:flutter/material.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({Key? key}) : super(key: key);

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();

    // Navega para a tela de login após 3 segundos
    Future.delayed(const Duration(seconds: 3), () {
      Navigator.pushReplacementNamed(context, '/login');
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        color: Colors.blue, // Cor de fundo
        child: Center(
          child: Container(
            decoration: const BoxDecoration(
              color: Colors.white, // Círculo branco
              shape: BoxShape.circle,
            ),
            padding: const EdgeInsets.all(20.0),
            child: Image.asset(
              'assets/logo.png', // Caminho para o logotipo
              width: 100,
              height: 100,
            ),
          ),
        ),
      ),
    );
  }
}