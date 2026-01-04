<script>
document.getElementById('transactionModal').addEventListener('show.bs.modal', function (event) {
    const btn = event.relatedTarget;

    document.getElementById('mProvider').textContent = btn.dataset.provider;
    document.getElementById('mTransaction').textContent = btn.dataset.transaction;
    document.getElementById('mItem').textContent = btn.dataset.item;
    document.getElementById('mItemId').textContent = btn.dataset.itemid;
    document.getElementById('mQty').textContent = btn.dataset.qty;
    document.getElementById('mAmount').textContent = 'R' + btn.dataset.amount;
    document.getElementById('mStatus').textContent = btn.dataset.status;
    document.getElementById('mDate').textContent = btn.dataset.date;
    document.getElementById('mDescription').textContent = btn.dataset.description;
    document.getElementById('mQr').src = btn.dataset.qr;
});
</script>
