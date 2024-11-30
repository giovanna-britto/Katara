import 'package:flutter/material.dart';

class PlantacaoCard extends StatelessWidget {
  final String titulo;
  final String proximaIrrigacao;
  final String quantidadeAgua;
  final String status;
  final String imagem; // Caminho da imagem

  const PlantacaoCard({
    Key? key,
    required this.titulo,
    required this.proximaIrrigacao,
    required this.quantidadeAgua,
    required this.status,
    required this.imagem, // Novo parâmetro
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(15),
      ),
      color: Colors.blue[200],
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            ClipRRect(
              borderRadius: BorderRadius.circular(10), // Arredondar as bordas da imagem
              child: Image.asset(
                imagem,
                width: 80,
                height: 80,
                fit: BoxFit.cover,
              ),
            ),
            const SizedBox(width: 16), // Espaçamento entre a imagem e o texto
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    titulo,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Colors.white,
                    ),
                  ),
                  const SizedBox(height: 8),
                  Text(
                    'Próxima Irrigação: $proximaIrrigacao',
                    style: const TextStyle(
                      fontSize: 16,
                      color: Colors.white,
                    ),
                  ),
                  Text(
                    'Quantidade de água: $quantidadeAgua',
                    style: const TextStyle(
                      fontSize: 16,
                      color: Colors.white,
                    ),
                  ),
                  Text(
                    status,
                    style: const TextStyle(
                      fontSize: 16,
                      color: Colors.white,
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}