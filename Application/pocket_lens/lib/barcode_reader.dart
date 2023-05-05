import 'package:flutter/material.dart';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';

class BarcodeReader extends StatelessWidget {
  const BarcodeReader({key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text('Barcode Scanner'),
        backgroundColor: const Color(0xFF106cb5),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () async {
          final barcode = await FlutterBarcodeScanner.scanBarcode(
            '#ff6666',
            'Cancel',
            true,
            ScanMode.BARCODE,
          );
          debugPrint("=======================BARCODE========================");
          debugPrint(barcode);
          debugPrint("======================================================");
        },
        child: const Icon(Icons.camera_alt),
      ),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
    );
  }
}
