import 'package:flutter/material.dart';

class DadosPlantacaoScreen extends StatelessWidget {
  const DadosPlantacaoScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    // Dados simulados (podem ser substituídos por dados reais da API)
    final plantacoes = [
      {
        "titulo": "Solo 1",
        "proximaIrrigacao": "18:00",
        "quantidadeAgua": "30 L",
        "status": "A terra precisa de mais adubo",
        "imagem": 'assets/solo1.jpg', // Adicione o caminho da imagem se disponível
      },
      {
        "titulo": "Solo 2",
        "proximaIrrigacao": "6:00",
        "quantidadeAgua": "50 L",
        "status": "A terra está saudável",
        "imagem": 'assets/solo2.jpg',
      },
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('Áreas'),
        backgroundColor: Colors.blue,
        centerTitle: true,
      ),
      body: Column(
        children: [
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16.0),
              itemCount: plantacoes.length,
              itemBuilder: (context, index) {
                final plantacao = plantacoes[index];
                return Card(
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(15),
                  ),
                  margin: const EdgeInsets.only(bottom: 16),
                  color: Colors.blue[100],
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                plantacao["titulo"]!,
                                style: const TextStyle(
                                  fontSize: 18,
                                  fontWeight: FontWeight.bold,
                                  color: Colors.blue,
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                "Próxima Irrigação: ${plantacao["proximaIrrigacao"]}",
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Colors.blueGrey,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                "Quantidade de água: ${plantacao["quantidadeAgua"]}",
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Colors.blueGrey,
                                ),
                              ),
                              const SizedBox(height: 4),
                              Text(
                                plantacao["status"]!,
                                style: const TextStyle(
                                  fontSize: 16,
                                  color: Colors.blueGrey,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: 16),
                        Container(
                          width: 50,
                          height: 50,
                          color: Colors.grey[300], // Placeholder para imagem
                          child: plantacao["imagem"] != null
                              ? Image.asset(
                            plantacao["imagem"]!,
                            fit: BoxFit.cover,
                          )
                              : const Icon(Icons.image, color: Colors.grey),
                        ),
                      ],
                    ),
                  ),
                );
              },
            ),
          ),
          ElevatedButton.icon(
            onPressed: () {
              // Navegar para a tela de cadastro
              Navigator.pushNamed(context, '/cadastro');
            },
            icon: const Icon(Icons.add),
            label: const Text('Adicionar Plantação'),
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.blue[100],
              foregroundColor: Colors.blue,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(10),
              ),
              padding: const EdgeInsets.symmetric(
                vertical: 15.0,
                horizontal: 30.0,
              ),
            ),
          ),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: 0, // Define o índice inicial como 0 (Início)
        items: const [
          BottomNavigationBarItem(
            icon: Icon(Icons.home),
            label: 'Início',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.chat),
            label: 'Chat',
          ),
          BottomNavigationBarItem(
            icon: Icon(Icons.bar_chart),
            label: 'Dashboard',
          ),
        ],
        selectedItemColor: Colors.blue,
        unselectedItemColor: Colors.grey,
        onTap: (index) {
          if (index == 0) {
            Navigator.pushReplacementNamed(context, '/home');
          } else if (index == 1) {
            Navigator.pushReplacementNamed(context, '/chat');
          } else if (index == 2) {
            Navigator.pushReplacementNamed(context, '/dashboard');
          }
        },
      ),
      backgroundColor: Colors.blue[50],
    );
  }
}