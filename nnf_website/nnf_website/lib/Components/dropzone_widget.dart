import 'package:flutter/material.dart';
import 'package:flutter_dropzone/flutter_dropzone.dart';
import 'package:nnf_website/Components/simple_async_button.dart';
import 'constants.dart';

class DropzoneWidget extends StatefulWidget {
  const DropzoneWidget({Key? key}) : super(key: key);

  //const DropzoneWidget({ Key? key }) : super(key: key);

  @override
  _DropzoneWidgetState createState() => _DropzoneWidgetState();
}

class _DropzoneWidgetState extends State<DropzoneWidget> {
  late DropzoneViewController controller;
  @override
  Widget build(BuildContext context) {
    
    Size size = MediaQuery.of(context).size;

    return Center(
      child: Container(
        margin: EdgeInsets.symmetric(vertical: size.height * 0.3, horizontal: size.width *0.1),
        padding: EdgeInsets.all(size.height * 0.025),
        decoration: BoxDecoration(
          color: kPrimaryColor,
          borderRadius: BorderRadius.circular(46)
        ),
        child: Stack(
          children: [
            DropzoneView(onDrop: acceptFile,),

            // DropzoneView(
            //   onCreated: (controller) => this.controller = controller,
            //   cursor: CursorType.grab,
            //   onDrop: acceptFile,
            //   //onHover:() => setState(()=> highlight = true),
            //   //onLeave: ()=> setState(()=>highlight = false),
            // ),
            Center(
              child: Column(
                //mainAxisSize: MainAxisSize.min,
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Padding(padding: const EdgeInsets.symmetric(vertical: 20),
                  child: Column(
                      children: const [
                        Icon(Icons.cloud_upload, size: 80, color: Colors.white,),
                        Text('Drop Files here', style: TextStyle(color: Colors.white, fontSize: 20),),
                      ],
                    ),
                  ),
                  
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 20),
                    child: SimpleAsyncButton(
                      text: 'Choose Files', 
                      press: () async {
                        final events = await controller.pickFiles();
                        if(events.isEmpty) return;

                        acceptFile(events.first);
                      },
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
  
  Future acceptFile(dynamic event) async{
    final name = event.name;
    final mime = await controller.getFileMIME(event);
    final bytes = await controller.getFileSize(event);
    final url = await controller.createFileUrl(event);
    print('Name: $name');
    print('Mime: $mime');
    print('Bytes: $bytes');
    print('Url: $url');

    // final droppedFile = DroppedFile(
    //   url: url,
    //   name: name,
    //   mime: mime,
    //   bytes: bytes,
    // );

  }
}
