import 'package:flutter/material.dart';
import '../widgets/plantacao_card.dart';
import 'cadastro_plantacao_screen.dart';

class DadosPlantacaoScreen extends StatelessWidget {
  const DadosPlantacaoScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Áreas'),
        backgroundColor: Colors.blue,
        centerTitle: true,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Expanded(
              child: ListView(
                children: [
                  PlantacaoCard(
                    titulo: 'Solo 1',
                    proximaIrrigacao: '18:00',
                    quantidadeAgua: '30 L',
                    status: 'A terra precisa de mais adubo',
                    imagem: 'assets/solo1.jpg', // Caminho da imagem
                  ),
                  const SizedBox(height: 16),
                  PlantacaoCard(
                    titulo: 'Solo 2',
                    proximaIrrigacao: '6:00',
                    quantidadeAgua: '50 L',
                    status: 'A terra está saudável',
                    imagem: 'assets/solo2.jpg', // Caminho da imagem
                  ),
                ],
              ),
            ),
            ElevatedButton.icon(
              onPressed: () {
                // Navegar para a tela de cadastro
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => const CadastroPlantacaoScreen(),
                  ),
                );
              },
              icon: const Icon(Icons.add),
              label: const Text('Adicionar máquina'),
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.blue[100],
                foregroundColor: Colors.blue,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(10),
                ),
              ),
            ),
          ],
        ),
      ),
      backgroundColor: Colors.blue[50],
    );
  }
}