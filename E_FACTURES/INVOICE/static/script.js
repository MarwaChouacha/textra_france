$(async () => {
    const navigation=[
        { id: 0, text: 'Acceuil', icon: 'chart' },

        { id: 1, text: 'Upload Facture', icon: 'upload' },
        { id: 2, text: 'Liste des Factures ', icon: 'menu' },
    ]
    const popup = $("#uploadPopup").dxPopup({
        title: "Uploader un fichier",
        visible: false,
        width: 400,
        height: 250,
        showCloseButton: true,
        contentTemplate: function () {
            return $("<div>").dxFileUploader({
                name: "file",
                multiple: false,
                uploadMode: "instantly", // or "useButtons"
                uploadUrl: "http://localhost:8000/api/upload/", // 🔁 adapte à ton endpoint
                onUploaded: function(e) {
                    DevExpress.ui.notify("Fichier uploadé avec succès", "success", 2000);
                    popup.hide();
                    $("#facture_div").dxDataGrid('instance').refresh()
                },
                onUploadError: function(e) {
                    DevExpress.ui.notify("Erreur lors de l'upload", "error", 2000);
                },
                
            });
        }
    }).dxPopup("instance");

    const popupPDF = $("#popup_view_pdf").dxPopup({
            title: "Aperçu de la Facture",
            visible: false,
            showCloseButton: true,
            width:'80%',
            height: "90%",
            contentTemplate: function () {
                // return $("<iframe id='pdf_viewer' style='width:100%;height:100%;border:none; object-fit: contain'>");
                //  return $("<img id='pdf_viewer' style='display:block; max-width:100%; height:auto;' />");
                return $("<div>", {
                    style: "width: 100%; height: 100%; overflow-y: auto; text-align: center;"
                }).append(
                    $("<img>", {
                        id: "pdf_viewer",
                        style: "max-width: 100%; height: auto; display: inline-block;"
                    })
                );
            }
        }).dxPopup("instance");
    
   

    const drawer = $('#drawer').dxDrawer({
    opened: true,
    height: '100%',
    closeOnOutsideClick: true,
    template() {
      const $list = $('<div style="background-color:#f0f0f0;color :white">').width(200).addClass('panel-list');
      return $list.dxList({
        dataSource: navigation,
        hoverStateEnabled: false,
        focusStateEnabled: false,
        activeStateEnabled: false,
        onItemClick(e) {
          const clickedItem = e.itemData;
          if (clickedItem.id === 1) {
            popup.show();
          } else 
          if (clickedItem.id === 2) {
            try{
                $("#report").css('display','none');
                $("#facture_div").dxDataGrid('dispose')
            }catch{

            }
                 const factureStore = new DevExpress.data.CustomStore({
                    key: "id",
                    load: async () => {
                        const response = await fetch("http://localhost:8000/api/factures/");
                        return await response.json();
                    },
                    update: async (key, values) => {
                        console.log("Updating facture ID:", key);
                        console.log("New values:", values);
                        const response = await fetch(`http://localhost:8000/api/factures/${key}/`, {
                            method: "PATCH",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify(values)
                        });
                        if (!response.ok) throw new Error("Update failed");
                        return await response.json();
                    },
                    remove: async (key) => {
                        const response = await fetch(`http://localhost:8000/api/factures/${key}/`, {
                            method: "DELETE"
                        });
                        if (!response.ok) throw new Error("Delete failed");
                    }
                });
    const dataGrid= $("#facture_div").dxDataGrid({
                dataSource: factureStore,
                // keyExpr: "id",
                columns: [
                    {
                        type: "buttons",
                        width: 100, // ajuste si nécessaire
                        buttons: [
                            "edit",    // ✏️ Modifier
                            "delete",  // ❌ Supprimer
                            "save",    // 💾 Sauvegarder (si mode "row")
                            "cancel",   // 🔄 Annuler (si mode "row")
                            {
                                hint: "Afficher facture",
                                icon: "fa fa-eye", // DevExtreme built-in icon
                                onClick: function(e) {
                                    const facture = e.row.data;
                                    console.log(facture)
                                    const pdfUrl =`/media/${facture.path}`;
                                    // const viewerUrl = `https://docs.google.com/viewer?embedded=true&url=${pdfUrl}`;
                                    
                                    popupPDF.show();

                                    setTimeout(() => {
                                        $("#pdf_viewer").attr("src", pdfUrl);
                                        // $("#pdf_viewer").on('load', function() {
                                        // const iframeDoc = this.contentDocument || this.contentWindow.document;
                                        // if(iframeDoc && iframeDoc.body && iframeDoc.body.firstElementChild){
                                        //     $(iframeDoc.body.firstElementChild).css('width', '80%');
                                        //     $(iframeDoc.body.firstElementChild).css('heigth', '100%');
                                        // }
                                        // });
                                    }, 100); // 100ms ça suffit souvent
                                }
                            }
                        ]
                    },
                    { dataField: "num", caption: "N° Facture" },
                    { dataField: "datefact", caption: "Date" },
                    { dataField: "textfact", visible: false }, // 🔴 Masquée
                    { dataField: "total", caption: "Montant Total" },
                    { dataField: "tva", caption: "Montant Tva" },
                    { dataField: "details", caption: "Détails" },
                    { dataField: "compte", caption: "Compte Comptable" },
                    { dataField: "categ", caption: "Catégorie" },
                    { dataField: "path", visible: true },
                ],
                rowAlternationEnabled: true,
                columnAutoWidth: true,
                editing: {
                    mode: "form",
                    allowUpdating: true,
                    allowAdding: false,
                    allowDeleting: true,
                    useIcons: true
                },
                paging: {
                    pageSize: 10
                },
                filterRow: {
                    visible: true
                },
                searchPanel: {
                    visible: true
                },
                headerFilter: {
                    visible: true
                },
                selection:{mode:'single'},
                onToolbarPreparing: function(e) {
                    // e.toolbarOptions.items.unshift({
                    //     location: "after",
                    //     widget: "dxButton",
                    //     options: {
                    //         icon: "upload",
                    //         // text: "Upload",
                    //         hint:'upload facture',

                    //         onClick: function() {
                    //             // 👉 Ton action ici (ex: ouvrir un input file)
                    //             popup.show();
                    //             // Tu peux aussi déclencher un fichier input ici
                    //         }
                    //     }
                    // });
                    e.toolbarOptions.items.unshift({
                        location: "after",
                        widget: "dxButton",
                        options: {
                            icon: "file",
                            hint:'identifier compte comptable',

                            // text: "Upload",
                            onClick: function() {
                                const selectedRowData = $("#facture_div").dxDataGrid("instance").getSelectedRowsData();
                    
                                if (selectedRowData.length === 0) {
                                    DevExpress.ui.notify("Veuillez sélectionner un compte", "error", 2000);
                                    return;
                                }
                                const selectedItem = selectedRowData[0]; // Assuming only one item is selected

                                // Prepare the data to send to the server
                                const dataToSend = {
                                    num: selectedItem.num,
                                    datefact: selectedItem.datefact,
                                    total: selectedItem.total,
                                    categ: selectedItem.categ,
                                    details:selectedItem.textfact
                                };
                                (async () => {
                        try {
                            const response = await fetch("http://localhost:8000/api/identcompte/", {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(dataToSend),
                            });

                                if (!response.ok) throw new Error("Fetch failed");

                                const data = await response.json();
                                if(data==1){
                                    DevExpress.ui.notify("Comptes synchronisés avec succès", "success", 2000);

                                }else{
                                DevExpress.ui.notify("Comptes not found", "warning", 2000);

                                }
                                console.log("Data sent successfully:", data);
                                $("#facture_div").dxDataGrid("instance").refresh()

                                // Optional: Show result to user
                            } catch (error) {
                                console.error("Erreur lors de la synchronisation:", error);
                                DevExpress.ui.notify("Échec de la synchronisation", "error", 2000);
                            }
                        })();
                            }
                        }
                    });
                }
                }).dxDataGrid('instance');
              
                dataGrid.refresh();
                
          }else if(clickedItem.id==0){
            try{
                 $("#report").css('display','none');
                 $("#facture_div").dxDataGrid('dispose')
            }catch{

            }
            $("#report").css('display','block');
            loadDashbord()
           
          }
        }
      });
    },
    }).dxDrawer('instance');
    $('#toolbar').dxToolbar({
    items: [{
      widget: 'dxButton',
      location: 'before',
      options: {
        icon: 'menu',
        stylingMode: 'text',
        onClick() {
          drawer.toggle();
        },
      },
    }],
  });


    loadDashbord()


});

function groupByMonth(data) {
  const grouped = {};
  console.log(data)

  data.forEach(f => {
    const date = new Date(f.date);
    const monthKey = `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}`;

    if (!grouped[monthKey]) {
      grouped[monthKey] = { month: monthKey, ttc: 0, tva: 0 };
    }

    grouped[monthKey].ttc += f.ttc;
    grouped[monthKey].tva += f.tva;
  });

  return Object.values(grouped).sort((a, b) => a.month.localeCompare(b.month));
}

async function loadDashbord(){
    
        const response = await fetch("http://localhost:8000/api/dashbord/",{method:'POST'});
        const data = await response.json();
        console.log(data)
        $('#ttc').text(data['totaux']['total_ttc'].toLocaleString('fr-FR') +' EUR')
        $('#tva').text(data['totaux']['total_tva'].toLocaleString('fr-FR')  +' EUR')
        $('#fact').text(data['totaux']['nbr_fact'] +' Facture(s)')
        $('#chart1').dxChart({
    dataSource:groupByMonth( data['totaux']['data1']),
    commonSeriesSettings: {
      argumentField: "month",
      type: "line"
    },
    series: [
      { valueField: "ttc", name: "Total TTC" },
      { valueField: "tva", name: "Total TVA" }
    ],
    legend: {
      verticalAlignment: "bottom",
      horizontalAlignment: "center"
    },
    title: "Total TTC et TVA par Mois",
    argumentAxis: {
      label: {
        format: "month"
      }
    },
    tooltip: {
      enabled: true,
      format: {
        type: "fixedPoint",
        precision: 2
      }
    }
  }) 

    //   $("#chart2").dxChart({
    //     dataSource: data['totaux']['data2'],
    //     series: {
    //       argumentField: "categ",
    //       valueField: "count",
    //       name: "Nombre de Factures",
    //       type: "bar",
    //       color: "#ffaa66"
    //     },
    //     title: "Nombre de Factures par Catégorie",
    //     tooltip: {
    //       enabled: true
    //     },
    //     legend: {
    //       visible: false
    //     }
    //   });

$("#chart2").dxPieChart({
    dataSource: data['totaux']['data2'],
    palette: "Soft",
    title: "Répartition des Factures par Catégorie",
    series: {
      argumentField: "categ",
      valueField: "count",
      label: {
        visible: true,
        connector: {
          visible: true,
          width: 1
        },
        format: "fixedPoint",
        customizeText: function (arg) {
          return arg.argument + ": " + arg.value;
        }
      }
    },
    tooltip: {
      enabled: true,
      format: "fixedPoint",
      customizeTooltip: function(arg) {
        return {
          text: `${arg.argumentText}: ${arg.valueText} factures`
        };
      }
    },
    legend: {
      orientation: "horizontal",
      itemTextPosition: "right",
      horizontalAlignment: "center",
      verticalAlignment: "bottom"
    }
  });
                    
}





